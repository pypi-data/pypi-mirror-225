# -*- coding: utf-8 -*-
#
# This file is part of the bliss project
#
# Copyright (c) 2015-2023 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

"""
Definition of classes representing a set of common functionalities for
monochromator control.

We assume that a monochromator is composed of:
    - Rotation motor (bragg angle - real motor)
    - Energy motor (Calc Motor)
    - Crystal(s)

The corresponding classes are MonochromatorBase, XtalManager and EnergyCalcMotor.
Configuration examples can be found in:
https://bliss.gitlab-pages.esrf.fr/bliss/master/config_mono.html
"""

import numpy
import tabulate

from bliss.common.types import IterableNamespace
from bliss.common.utils import autocomplete_property
from bliss.common.protocols import HasMetadataForDataset, HasMetadataForScan
from bliss.common.utils import BOLD

from bliss.physics.units import ur
from bliss.controllers.bliss_controller import BlissController
from bliss.shell.standard import umv

from bliss.controllers.monochromator.xtal import MonochromatorXtals, XtalManager


class Monochromator(BlissController, HasMetadataForScan, HasMetadataForDataset):
    """
    Monochromator
    """

    def __init__(self, config):

        super().__init__(config)

        # Motors
        self._motors = {"energy": None, "bragg": None, "bragg_rotation": None}

        # Trackers
        tracker = config.get("tracker", None)
        if tracker is not None:
            self.tracking = tracker
            self.tracking._set_mono(self)

    @autocomplete_property
    def motors(self):
        return IterableNamespace(**self._motors)

    def _close(self):
        self.__close__()

    def __close__(self):
        for motor in filter(None, self.motors):
            if hasattr(motor, "__close__"):
                motor.__close__()

    def _load_config(self):
        """Load Configuration"""

        # Motors
        motors_conf = self.config.get("motors", None)
        if motors_conf is None:
            raise ValueError(
                f"Monochromator {BOLD(self._name)}: No Energy motor in config"
            )
        for motor_conf in motors_conf:
            for key in motor_conf.keys():
                motor = motor_conf.get(key)
                # Energy
                if key == "energy":
                    self._motors["energy"] = motor
                    motor.controller._set_mono(self)
                elif key == "energy_tracker":
                    self._motors["energy_tracker"] = motor
                    motor.controller._set_mono(self)
                elif "bragg_rotation" in motor_conf.keys():
                    self._motors["bragg_rotation"] = motor
                else:
                    self._motors[key] = motor
                    if hasattr(motor.controller, "_set_mono"):
                        motor.controller._set_mono(self)

        if self._motors["energy"] is None:
            raise ValueError(
                f"Monochromator {BOLD(self._name)}: No Energy motor in config"
            )
        # Bragg
        for axis in self._motors["energy"].controller.reals:
            if self._motors["energy"].controller._axis_tag(axis) == "bragg":
                self._motors["bragg"] = axis
        if self._motors["bragg"] is None:
            raise ValueError(
                f"Monochromator {BOLD(self._name)}: Energy motor does not reference Bragg motor"
            )
        if self._motors["bragg_rotation"] is None:
            self._motors["bragg_rotation"] = self._motors["bragg"]

        # Xtals Object
        self._load_config_xtal()

    def _load_config_xtal(self):
        self._available_xtals = self.config.get("available_xtals", None)
        self._xtals = self.config.get("xtals", None)
        if self._available_xtals is None:
            if self._xtals is None:
                raise RuntimeError("No xtals configured")
            if len(self._xtals.xtal_names) == 0:
                raise RuntimeError("No Crystals Defined in the XtalManager")
            self._available_xtals = self._xtals.xtal_names
        else:
            if self._xtals is not None:
                if len(self._xtals.xtal_names) == 0:
                    raise RuntimeError("No Crystals Defined in the XtalManager")
                for xtal_name in self._available_xtals:
                    if xtal_name not in self._xtals.xtal_names:
                        raise RuntimeError(
                            f'Xtal "{xtal_name}" not defined in the XtalManager'
                        )
            else:
                xtal_conf = {"name": f"{self.name}_xtals", "xtals": []}
                for xtal_name in self._available_xtals:
                    xtal_conf["xtals"].append({"xtal": xtal_name})
                self._xtals = XtalManager(xtal_conf)
        if len(self._available_xtals) > 1:
            self.xtal = MonochromatorXtals(self, self._available_xtals)

    #
    # Initialization

    def _init(self):
        # Force unit definition for energy and bragg motors
        assert self._motors["energy"].unit, "Please specify unit for the Energy motor"
        assert self._motors["bragg"].unit, "Please specify unit for the Bragg motor"

        # Manage selected xtal
        self._xtal_init()

    def _xtal_init(self):
        """Chrystals initializaton"""
        xtal = self._xtals.xtal_sel
        if xtal is not None:
            if not self._xtal_is_in(xtal):
                self._xtals.xtal_sel = None
                for xtal in self._xtals.xtal_names:
                    if self._xtal_is_in(xtal):
                        self._xtals.xtal_sel = xtal
                        return
        else:
            for xtal in self._xtals.xtal_names:
                if self._xtal_is_in(xtal):
                    self._xtals.xtal_sel = xtal
                    return

    #
    # User Info

    def __info__(self):
        info_str = "\n"
        info_str += self._info_mono()
        info_str += self._info_xtals()
        info_str += self._info_motor_energy()
        info_str += self._info_motor_tracking()
        info_str += "\n"
        return info_str

    def _info_mono(self):
        """Get the monochromator information."""
        return f"Monochromator: {self._name}\n\n"

    def _info_xtals(self):
        """Get the chrystal information."""
        xtal = self._xtals.xtal_sel
        xtals = " ".join(self._available_xtals)
        mystr = f"Crystal: {xtal} ({xtals})\n\n"
        return mystr

    def _info_motor_tracking(self):
        info_str = ""
        if hasattr(self, "tracking"):
            controller = self._motors["energy_tracker"].controller
            # TITLE
            title = [""]
            for axis in controller.pseudos:
                title.append(axis.name)
            for axis in controller.reals:
                title.append(axis.name)
            # CALCULATED POSITION ROW
            calculated = ["Calculated"]
            val = self.bragg2energy(self._motors["bragg_rotation"].position)
            valu = self._motors["energy"].unit
            calculated.append(f"{val:.3f} {valu}")
            for axis in controller.reals:
                if controller._axis_tag(axis) == "energy":
                    calculated.append(f"{val:.3f} {valu}")
                else:
                    calculated.append(
                        f"{axis.tracking.energy2tracker(val):.3f} {axis.unit}"
                    )
            # CURRENT POSITION ROW
            current = ["Current"]
            current.append(
                f"{controller.pseudos[0].position:.3f} {controller.pseudos[0].unit}"
            )
            for axis in controller.reals:
                current.append(f"{axis.position:.3f} {axis.unit}")
            # TRACKING STATE ROW
            tracking = ["Tracking", "", ""]
            for axis in controller.reals:
                if controller._axis_tag(axis) != "energy":
                    if axis.tracking.state:
                        tracking.append("ON")
                    else:
                        tracking.append("OFF")

            info_str = tabulate.tabulate(
                [calculated, current, tracking],
                headers=title,
                tablefmt="plain",
                stralign="right",
            )
        return f"{info_str}\n"

    def _info_motor_energy(self):
        # TITLE
        title = [""]
        title.append(self._motors["energy"].name)
        title.append(self._motors["bragg"].name)
        # CALCULATED POSITION ROW
        calculated = ["Calculated"]
        # energy
        val = self.bragg2energy(self._motors["bragg_rotation"].position)
        valu = self._motors["energy"].unit
        calculated.append(f"{val:.3f} {valu}")
        # bragg
        val = self._motors["bragg_rotation"].position
        valu = self._motors["bragg"].unit
        calculated.append(f"{val:.3f} {valu}")
        #
        # CURRENT POSITION ROW
        #
        current = ["Current"]
        for motname in ["energy", "bragg"]:
            val = self._motors[motname].position
            valu = self._motors[motname].unit
            current.append(f"{val:.3f} {valu}")

        info_str = tabulate.tabulate(
            [calculated, current], headers=title, tablefmt="plain", stralign="right"
        )
        return f"{info_str}\n\n"

    #
    # Xtals

    def _xtal_is_in(self, xtal):
        """
        To be overloaded to reflect the monochromator behaviour
        """
        return True

    def _xtal_change(self, xtal):
        """
        To be overloaded to reflect the monochromator behaviour
        """

    #
    # Energy related methods

    def setE(self, energy):
        """
        For SPEC compatibility:
        This method change the offset of the Bragg motor to fit with an energy
        which has been positioned using a known sample.
        Remarks:
            - The mono need to be at the given energy.
            - In case of the bragg motor being a CalcMotor, do not forget
              to foresee the set offset method in it.
        """
        new_bragg = self.energy2bragg(energy)
        old_bragg = self._motors["bragg"].dial
        offset = new_bragg - old_bragg
        self._motors["bragg"].offset = offset
        self._motors["energy"].controller.sync_pseudos()

    def energy2bragg(self, energy):
        """Calculate the bragg angle as function of the energy.
        Args:
            energy(float): Energy value in the units of the energy motor.
        Returns:
            (float): Bragg angle value in the units of the bragg motor
        """
        energy_unit = energy * ur.Unit(self._motors["energy"].unit)
        # convert energy in keV
        energy_keV = energy_unit.to("keV").magnitude
        bragg_deg = self._xtals.energy2bragg(energy_keV) * ur.deg
        # returned bragg angle value is in deg, convert in motor units
        bragg_unit = bragg_deg.to(self._motors["bragg"].unit)
        return bragg_unit.magnitude

    def bragg2energy(self, bragg):
        """Calculate bragg angle for given energy.
        Args:
            bragg (float): Bragg angle value in the units of the bragg motor.
        Retuns:
            (float): Energy value in the units of the energy motor.
        """
        bragg_unit = bragg * ur.Unit(self._motors["bragg"].unit)
        # covert bragg in deg
        bragg_deg = bragg_unit.to("deg").magnitude
        energy_keV = self._xtals.bragg2energy(bragg_deg) * ur.keV
        # returned value is in keV, convert in motor units
        energy_unit = energy_keV.to(self._motors["energy"].unit)
        return energy_unit.magnitude

    #
    # Metadata

    def dataset_metadata(self) -> dict:
        mdata = {"name": self._name}
        xtal = self._xtals.xtal_sel
        if xtal is None:
            return mdata
        theta = self._motors["bragg"].position
        unit = self._motors["bragg"].unit or "deg"
        theta = theta * ur.parse_units(unit)
        mdata.update(self._xtals.get_metadata(theta))
        return mdata

    def scan_metadata(self) -> dict:
        mdata = self.dataset_metadata()
        mdata.pop("name")
        mdata["@NX_class"] = "NXmonochromator"
        if "energy" in mdata:
            mdata["energy@units"] = "keV"
        if "wavelength" in mdata:
            mdata["wavelength@units"] = "m"
        crystal = mdata.get("crystal")
        if crystal:
            crystal["@NX_class"] = "NXcrystal"
            crystal["d_spacing@units"] = "m"
        return mdata


class MonochromatorFixExit(Monochromator):
    """Fixed exit monochromatot"""

    def _load_config(self):
        """Load Configuration"""

        super()._load_config()

        # Fix exit Parameter
        self._fix_exit_offset = self.config.get("fix_exit_offset", None)

    def __info__(self):
        info_str = "\n"
        info_str += self._info_mono()
        info_str += self._info_xtals()
        info_str += self._info_motor_energy()
        info_str += self._info_motor_tracking()
        info_str += "\n"
        return info_str

    def _info_xtals(self):
        xtal = self._xtals.xtal_sel
        xtals = " ".join(self._available_xtals)
        if hasattr(self, "fix_exit_offset"):
            mystr = f"Crystal         : {xtal} ({xtals})\n"
            mystr += f"Fix exit_offset : {self.fix_exit_offset}\n\n"
        else:
            mystr = f"Crystal : {xtal} ({xtals})\n"
        return mystr

    """
    Energy related methods, specific to Fix Exit Mono
    """

    @property
    def fix_exit_offset(self):
        return self._fix_exit_offset

    @fix_exit_offset.setter
    def fix_exit_offset(self, value):
        self._fix_exit_offset = value

    def bragg2dxtal(self, bragg):
        if self.fix_exit_offset is not None:
            dxtal = numpy.abs(self.fix_exit_offset) / (
                2.0 * numpy.cos(numpy.radians(bragg))
            )
            return dxtal
        raise RuntimeError("No Fix Exit Offset parameter defined (config)")

    def dxtal2bragg(self, dxtal):
        if self.fix_exit_offset is not None:
            bragg = numpy.degrees(
                numpy.arccos(numpy.abs(self.fix_exit_offset) / (2.0 * dxtal))
            )
            return bragg
        raise RuntimeError("No Fix Exit Offset parameter defined (config)")

    def energy2dxtal(self, ene):
        bragg = self.energy2bragg(ene)
        dxtal = self.bragg2dxtal(bragg)
        return dxtal


class SimulMonoWithChangeXtalMotors(Monochromator):
    """Simulation monochromator which implements the _xtal_is_in() and
    _xtal_change() to move few motors to configured (YML) positions where a
    single bragg motor can rotate several crystal.
    For instance a multilayer or a channel-cut monochromators can be equiped
    with 2 different crystals and one should shift a vertical and a horizontal
    translation to put the selected crystal into the beam. In addition to the
    translations a offset on the bragg motor is applied to take care of a
    mechanical miss-alignment in angle of the 2 crystal surfaces.
    """

    def _load_config(self):
        """Load Configuration"""

        super()._load_config()

        self._ver_target = {}
        self._hor_target = {}
        self._bragg_offset = {}

        self._ver_motor = self.config.get("ver_motor")
        self._hor_motor = self.config.get("hor_motor")
        self._ver_tolerance = self.config.get("ver_tolerance")
        self._hor_tolerance = self.config.get("hor_tolerance")
        self._ver_target = self._xtals.get_xtals_config("ver_target")
        self._hor_target = self._xtals.get_xtals_config("hor_target")
        self._bragg_offset = self._xtals.get_xtals_config("bragg_offset")

    def _xtal_is_in(self, xtal):
        ver_pos = self._ver_motor.position
        hor_pos = self._hor_motor.position

        in_pos = True
        if xtal in self._hor_target.keys():
            if not numpy.isclose(
                hor_pos, self._hor_target[xtal], atol=self._hor_tolerance
            ):
                in_pos = False
        if xtal in self._ver_target.keys():
            if not numpy.isclose(
                ver_pos, self._ver_target[xtal], atol=self._ver_tolerance
            ):
                in_pos = False

        return in_pos

    def _xtal_change(self, xtal):
        mv_list = []
        if xtal in self._hor_target.keys():
            mv_list.append(self._hor_motor)
            mv_list.append(self._hor_target[xtal])
        if xtal in self._ver_target.keys():
            mv_list.append(self._ver_motor)
            mv_list.append(self._ver_target[xtal])

        if xtal in self._bragg_offset.keys():
            self._motors["bragg"].offset = self._bragg_offset[xtal]

        if len(mv_list) > 0:
            umv(*mv_list)
