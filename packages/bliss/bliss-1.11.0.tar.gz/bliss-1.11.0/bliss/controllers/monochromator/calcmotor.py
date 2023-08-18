# -*- coding: utf-8 -*-
#
# This file is part of the bliss project
#
# Copyright (c) 2015-2023 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

"""Calculation motors classes. This is part of the monochromator control."""

import numpy

from bliss.controllers.motor import CalcController


class MonochromatorCalcMotorBase(CalcController):
    """Base class"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._mono = None

        if "approximation" in self.config.config_dict:
            self.approx = float(self.config.get("approximation"))
        else:
            self.approx = 0.0

    def __info__(self):
        info_str = f"CONTROLLER: {self.__class__.__name__}\n"
        return info_str

    def get_axis_info(self, axis):
        """Get the info for axis"""
        info_str = ""
        return info_str

    def _set_mono(self, mono):
        """Define mono property"""
        self._mono = mono

    def _pseudos_are_moving(self):
        """Check if pseudo axis are moving"""
        for axis in self.pseudos:
            if axis.is_moving:
                return True
        return False


class EnergyCalcMotor(MonochromatorCalcMotorBase):
    """Energy Calculation Motor"""

    def calc_from_real(self, real_positions):
        """Calculate the energy from the position of the real motor.
           The real motor value is in the units of the real motor.
           The energy value is in the units of the enetgy motor.
        Args:
            real_positions(dict): Dictionary of the real motor position(s).
        Returns:
            (dict): Dictionary with the energy position(s)
        """
        pseudos_dict = {}

        if self._mono is not None and self._mono._xtals.xtal_sel is not None:
            ene = self._mono.bragg2energy(real_positions["bragg"])
            pseudos_dict["energy"] = ene
        else:
            pseudos_dict["energy"] = numpy.nan
        return pseudos_dict

    def calc_to_real(self, positions_dict):
        """Calculate the position of the real motor from the energy.
           The energy value is in the units of the enetgy motor.
           The real motor value is in the units of the real motor.
        Args:
            positions_dict (dict): Dictionary with the energy position(s)
        Returns:
            (dict): Dictionary of the real motor position(s).
        """
        reals_dict = {}
        if (
            self._mono is not None
            and self._mono._xtals.xtal_sel is not None
            and not numpy.isnan(positions_dict["energy"]).any()
        ):
            reals_dict["bragg"] = self._mono.energy2bragg(positions_dict["energy"])
        else:
            for axis in self.reals:
                reals_dict[self._axis_tag(axis)] = axis.position
        return reals_dict


class BraggFixExitCalcMotor(MonochromatorCalcMotorBase):
    """
    Bragg Fix Exit Calculation Motor
    """

    def calc_from_real(self, real_positions):

        pseudos_dict = {}

        if self._mono is not None:
            bragg = self._mono.xtal2bragg(real_positions["xtal"])
            rbragg = real_positions["bragg"]

            if (
                numpy.isclose(bragg, rbragg, atol=self.approx)
            ) or self._pseudos_are_moving():
                pseudos_dict["bragg_fix_exit"] = real_positions["bragg"]
            else:
                pseudos_dict["bragg_fix_exit"] = numpy.nan
        else:
            pseudos_dict["bragg_fix_exit"] = numpy.nan

        return pseudos_dict

    def calc_to_real(self, positions_dict):

        reals_dict = {}

        if (
            self._mono is not None
            and not numpy.isnan(positions_dict["bragg_fix_exit"]).any()
        ):
            reals_dict["bragg"] = positions_dict["bragg_fix_exit"]
            reals_dict["xtal"] = self._mono.bragg2xtal(positions_dict["bragg_fix_exit"])
        else:
            for axis in self.reals:
                reals_dict[self._axis_tag(axis)] = axis.position

        return reals_dict


class MonochromatorTrackerCalcMotorBase(MonochromatorCalcMotorBase):
    """
    - all tracker real motors must contain "tracker" in their tag name
    - master tracker calculation motor must be <master_real_tag_name>_tracker
    - The real motor tagged <master> will be the scanned motor
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._master_tag = self.config.get("master_tag")
        self._master_tracker_tag = f"{self._master_tag}_tracker"

    def _init(self):
        super()._init()
        for axis in self.reals:
            tag = self._axis_tag(axis)
            if tag == self._master_tag:
                self._master_motor = axis
        for axis in self.pseudos:
            tag = self._axis_tag(axis)
            if tag == self._master_tracker_tag:
                self._calc_motor = axis

    def get_master_motor(self):
        return self._master_motor

    def master2energy(self, master_pos):
        raise NotImplementedError

    def master2energy_dial(self, master_pos):
        raise NotImplementedError

    def get_acquisition_master(self, start, stop, nb_points, time_per_point):
        raise NotImplementedError

    def tracker_in_position(self, energy, reals_dict):
        in_pos = True
        for axis in self.reals:
            tag = self._axis_tag(axis)
            if tag.find("tracker") != -1:
                if axis.tracking.state:
                    track = axis.tracking.energy2tracker(energy)
                    rtrack = reals_dict[tag]
                    if not numpy.isclose(track, rtrack, atol=self.approx):
                        in_pos = False
        return in_pos

    def set_reals_current_position(self):
        reals_dict = {}
        for axis in self.reals:
            reals_dict[self._axis_tag(axis)] = axis.position
        return reals_dict

    def calc_from_real(self, reals_dict):

        pseudos_dict = {}

        energy_dial = self.master2energy_dial(reals_dict[self._master_tag])

        in_pos = self.tracker_in_position(energy_dial, reals_dict)

        if in_pos or self._pseudos_are_moving():
            pseudos_dict[self._master_tracker_tag] = reals_dict[self._master_tag]
        else:
            pseudos_dict[self._master_tracker_tag] = numpy.nan

        return pseudos_dict

    def calc_to_real(self, pseudos_dict):

        reals_dict = {}

        energy_dial = self.master2energy_dial(pseudos_dict[self._master_tracker_tag])

        if not numpy.isnan(pseudos_dict[self._master_tracker_tag]).any():
            reals_dict[self._master_tag] = pseudos_dict[self._master_tracker_tag]
            for axis in self.reals:
                tag = self._axis_tag(axis)
                if tag.find("tracker") != -1:
                    if axis.tracking.state:
                        reals_dict[tag] = axis.tracking.energy2tracker(energy_dial)
                    else:
                        reals_dict[tag] = axis.position
        else:
            reals_dict = self.set_reals_current_position()

        return reals_dict


class EnergyTrackerCalcMotor(MonochromatorTrackerCalcMotorBase):
    """
    Energy + Trackers Calculated motor
    Trajectory: Energy constant speed
    """

    def master2energy(self, energy_user):
        return energy_user

    def master2energy_dial(self, energy_user):
        bragg_motor = self._mono._motors["bragg"]
        bragg_offset = bragg_motor.offset
        bragg_user = self._mono.energy2bragg(energy_user)
        bragg_dial = bragg_user - bragg_offset
        energy_dial = self._mono.bragg2energy(bragg_dial)
        return energy_dial


class BraggTrackerCalcMotor(MonochromatorTrackerCalcMotorBase):
    """
    Bragg + Trackers Calculated motor
    Trajectory: Bragg constant speed
    """

    def master2energy(self, bragg_user):
        return self._mono.bragg2energy(bragg_user)

    def master2energy_dial(self, bragg_user):
        bragg_motor = self._mono._motors["bragg"]
        bragg_offset = bragg_motor.offset
        bragg_dial = bragg_user - bragg_offset
        return self._mono.bragg2energy(bragg_dial)
