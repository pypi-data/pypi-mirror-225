# -*- coding: utf-8 -*-
#
# This file is part of the bliss project
#
# Copyright (c) 2015-2023 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

"""
Module to manage scan with automatic filter.

Yaml config may look like this:
- plugin: bliss
  class: AutoFilter
  name: autof_eh1
  package: bliss.common.auto_filter
  detector_counter_name: roi1
  monitor_counter_name: mon
  min_count_rate: 20000
  max_count_rate: 50000
  energy_axis: $eccmono
  filterset: $filtW1

# optional parameters
  always_back: True
  counters:
    - counter_name: curratt
      tag: fiteridx
    - counter_name: transm
      tag: transmission
    - counter_name: ratio
      tag: ratio
  suffix_for_corr_counter: "_corr"
  counters_for_correction:
    - det
    - apdcnt
"""

from tabulate import tabulate
from bliss.config.beacon_object import BeaconObject
from bliss.config import static
from bliss.common.event import connect, disconnect
from bliss.common.measurementgroup import _get_counters_from_names
from bliss.common.utils import autocomplete_property
from bliss import global_map, current_session
from bliss.common.axis import Axis
from bliss.common.types import _countable
from bliss.common.protocols import counter_namespace, CounterContainer
from bliss.common.auto_filter.filterset import FilterSet
from bliss.common.auto_filter.counters import FilterSetCounterController
from bliss.common.auto_filter.counters import AutoFilterCalcCounterController
from bliss.common.auto_filter.counters import FilterSetCounter


def _unmarshalling_energy_axis(_, value):
    if isinstance(value, str):
        config = static.get_config()
        return config.get(value)
    else:
        return value


def _marshalling_energy_axis(_, value):
    return value.name


class AutoFilter(CounterContainer, BeaconObject):
    detector_counter_name = BeaconObject.property_setting(
        "detector_counter_name", doc="Detector counter name"
    )

    monitor_counter_name = BeaconObject.property_setting(
        "monitor_counter_name", doc="Monitor counter name"
    )

    @detector_counter_name.setter
    def detector_counter_name(self, counter_name):
        assert isinstance(counter_name, str)
        return counter_name

    @monitor_counter_name.setter
    def monitor_counter_name(self, counter_name):
        assert isinstance(counter_name, str)
        return counter_name

    @property
    def detector_counter(self):
        return self.__counter_getter(self.detector_counter_name)

    @detector_counter.setter
    def detector_counter(self, counter):
        self.detector_counter_name = self.__counter_setter(counter)

    @property
    def monitor_counter(self):
        return self.__counter_getter(self.monitor_counter_name)

    @monitor_counter.setter
    def monitor_counter(self, counter):
        self.monitor_counter_name = self.__counter_setter(counter)

    def __counter_getter(self, counter_name):
        if not counter_name:
            raise RuntimeError("Counter missing from configuration")
        counters, missing = _get_counters_from_names([counter_name])
        if missing:
            raise RuntimeError(f"Counter {repr(counter_name)} does not exist")
        return counters[0]

    def __counter_setter(self, counter):
        if isinstance(counter, str):
            # check that counter exists ... not sure if the next lines work in all cases
            try:
                global_map.get_counter_from_fullname(counter)
                return counter
            except AttributeError:
                raise RuntimeError(f"Counter {repr(counter)} does not exist") from None
        elif isinstance(counter, _countable):
            return counter.fullname
        else:
            raise RuntimeError(f"Unknown counter {counter}")

    min_count_rate = BeaconObject.property_setting(
        "min_count_rate",
        must_be_in_config=True,
        doc="Minimum allowed count rate on monitor",
    )

    @min_count_rate.setter
    def min_count_rate(self, value):
        self.__filterset_needs_sync = True

    max_count_rate = BeaconObject.property_setting(
        "max_count_rate",
        must_be_in_config=True,
        doc="Maximum allowed count rate on monitor",
    )

    @max_count_rate.setter
    def max_count_rate(self, value):
        self.__filterset_needs_sync = True

    always_back = BeaconObject.property_setting(
        "always_back",
        must_be_in_config=False,
        default=True,
        doc="Always move back the filter to the original position at the end of the scan",
    )

    corr_suffix = BeaconObject.property_setting(
        "corr_suffix",
        must_be_in_config=False,
        default="_corr",
        doc="suffix to be added to the corrected counters",
    )

    filterset = BeaconObject.config_obj_property_setting(
        "filterset", doc="filterset to attached to the autofilter"
    )

    @filterset.setter
    def filterset(self, new_filterset):
        assert isinstance(new_filterset, FilterSet)
        self.__filterset_needs_sync = True
        # as this is a config_obj_property_setting
        # the setter has to return the name of the
        # corresponding beacon object
        return new_filterset

    def __init__(self, name, config):
        super().__init__(config, share_hardware=False)
        global_map.register(self, tag=self.name, parents_list=["counters"])

        self.__create_counters(config)
        self.__counters_for_corr = set()
        self.counters_for_correction = config.get("counters_for_correction", [])

        self.__filterset_is_synchronized = False
        self.__filterset_needs_sync = True
        self._max_nb_iter = None

    def _set_energy_changed(self, new_energy):
        self.__filterset_needs_sync = True

    def __close__(self):
        energy_axis = self.energy_axis
        if energy_axis is not None:
            disconnect(energy_axis, "position", self._set_energy_changed)

    def initialize_filterset(self):
        filterset = self.filterset
        if self.always_back:
            filterset.filter_back = filterset.get_filter()

    def synchronize_filterset(self):
        if not self.__filterset_needs_sync:
            return
        filterset = self.filterset
        # Synchronize the filterset with countrate range and energy
        # and tell it to store back filter if necessary
        energy = self.energy_axis.position
        if energy <= 0:
            unit = self.energy_axis.unit
            raise RuntimeError(f"The current energy is not valid: {energy} {unit}")
        # filterset sync. method return the maximum effective number of filters
        # which will correspond to the maximum number of filter changes
        self._max_nb_iter = filterset.sync(
            self.min_count_rate, self.max_count_rate, energy, self.always_back
        )
        self.__filterset_needs_sync = False
        self.__filterset_is_synchronized = True

    @property
    def max_nb_iter(self):
        self.synchronize_filterset()
        return self._max_nb_iter

    def maximum_number_of_tries(self, scan_npoints):
        # the maximum would be `scan_npoints*self.max_nb_iter` but this
        # causes lima to take took much time in preparation
        return scan_npoints + (6 * self.max_nb_iter)

    energy_axis = BeaconObject.property_setting(
        "energy_axis",
        must_be_in_config=True,
        set_marshalling=_marshalling_energy_axis,
        set_unmarshalling=_unmarshalling_energy_axis,
    )

    @energy_axis.setter
    def energy_axis(self, energy_axis):
        previous_energy_axis = self.energy_axis
        if self._in_initialize_with_setting or energy_axis != previous_energy_axis:
            if isinstance(energy_axis, Axis):
                if previous_energy_axis is not None:
                    disconnect(
                        previous_energy_axis, "position", self._set_energy_changed
                    )
                connect(energy_axis, "position", self._set_energy_changed)
                self._set_energy_changed(energy_axis.position)
            else:
                raise ValueError(f"{energy_axis} is not a Bliss Axis")

    @property
    def counters_for_correction(self):
        """These counters will have an additional correction counter"""
        return list(self.__counters_for_corr)

    @counters_for_correction.setter
    def counters_for_correction(self, counters):
        if not isinstance(counters, list):
            counters = list(counters)
        # The monitor counter is the default, remove missing counters.
        cnts, missing = _get_counters_from_names(counters)
        for cnt in cnts:
            self.__counters_for_corr.add(cnt.fullname)

    @autocomplete_property
    def counters(self):
        counters = []
        if self.filterset_counter_controller is not None:
            counters += list(self.filterset_counter_controller.counters)
        if self.calc_counter_controller is not None:
            counters += list(self.calc_counter_controller.outputs)
        return counter_namespace(counters)

    @property
    def transmission(self):
        self.synchronize_filterset()
        return self.filterset.transmission

    @property
    def filter(self):
        return self.filterset.filter

    @filter.setter
    def filter(self, new_filter):
        self.__filterset_needs_sync = True
        self.filterset.filter = new_filter

    def __info__(self):
        table_info = []
        for sname in (
            "monitor_counter_name",
            "detector_counter_name",
            "min_count_rate",
            "max_count_rate",
            "always_back",
        ):
            table_info.append([sname, getattr(self, sname)])
        info = str(tabulate(table_info, headers=["Parameter", "Value"]))
        info += "\n\n" + f"Active filterset: {self.filterset.name}"
        info += (
            "\n"
            + f"Energy axis {self.energy_axis.name}: {self.energy_axis.position:.5g} keV"
        )

        # calling transmission can update the filterset info_table if the energy has changed
        transm = self.transmission

        info += (
            "\n\n"
            + f"Current filter idx {self.filterset.filter}, transmission {transm:g}"
        )

        info += "\n\n" + "Table of Effective Filters :"
        if self.__filterset_is_synchronized:
            info += "\n" + self.filterset.info_table()
        else:
            info += "\n Cannot get effective filters, check your energy, please !!!"
        return info

    def __create_counters(self, config, export_to_session=True):
        cnts_conf = config.get("counters")
        if cnts_conf is None:
            self.filterset_counter_controller = None
            self.calc_counter_controller = None
            return

        self.filterset_counter_controller = FilterSetCounterController(self)
        for counter_name, tag in self.iter_counter_names(config, skip_tags=["ratio"]):
            counter = self.filterset_counter_controller.create_counter(
                FilterSetCounter, counter_name, mode="SINGLE"
            )
            counter.tag = tag
            if export_to_session:
                self.__add_to_bliss_session(counter_name, counter)
        self.calc_counter_controller = AutoFilterCalcCounterController(self, config)

    def iter_counter_names(self, config, skip_tags=tuple(), only_tags=None):
        for conf in config.get("counters", list()):
            tag = conf["tag"].strip()
            if only_tags and tag not in only_tags:
                continue
            if tag in skip_tags:
                continue
            counter_name = conf["counter_name"].strip()
            yield counter_name, tag

    def __add_to_bliss_session(self, name, obj):
        if not current_session:
            return
        if (
            name in current_session.config.names_list
            or name in current_session.env_dict.keys()
        ):
            raise ValueError(
                f"Cannot export object to session with the name '{name}', name is already taken! "
            )
        current_session.env_dict[name] = obj

    def beam_attenuation_correction(self, point_nb, name, data):
        """Calculate signal that would have been measured when the primary
        beam was not attenuation.
        """
        return data / self.transmission

    def scan_metadata(self):
        meta_dict = {"@NX_class": "NXcollection"}
        meta_dict["monitor"] = self.monitor_counter_name
        meta_dict["detector"] = self.detector_counter_name
        meta_dict["min_count_rate"] = self.min_count_rate
        meta_dict["max_count_rate"] = self.max_count_rate
        meta_dict["filterset"] = self.filterset.name
        return meta_dict
