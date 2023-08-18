import numpy
from bliss.common.counter import SamplingCounter
from bliss.controllers.counter import SamplingCounterController
from bliss.controllers.counter import CalcCounterController
from bliss.controllers.counter import CalcCounter
from bliss.common.protocols import counter_namespace
from bliss.common.protocols import HasMetadataForScanExclusive


class FilterSetCounter(SamplingCounter):
    pass


class AutoFilterCalcCounter(CalcCounter):
    pass


class FilterSetCounterController(
    SamplingCounterController, HasMetadataForScanExclusive
):
    """Manages auto filter counters.

    It use the following tags:
    - filteridx: position of the filterset
    - transmission: transmission of the filterset
    """

    def __init__(self, auto_filter):
        super().__init__(auto_filter.name)
        self.__auto_filter = auto_filter

    def read_all(self, *counters):
        values = []
        for cnt in counters:
            if cnt.tag == "filteridx":
                values.append(self.__auto_filter.filterset.get_filter())
            elif cnt.tag == "transmission":
                values.append(self.__auto_filter.transmission)
        return values

    def scan_metadata(self):
        return self.__auto_filter.scan_metadata()


class AutoFilterCalcCounterController(CalcCounterController):
    """Manages auto filter calculation counters.

    It use the following tags:
    - detector_corr: autofilter "detector" divided by "transmission"
                     Note: primary beam attebuation correction
    - ratio: "detector_corr" divided by autofilter "monitor"
    """

    def __init__(self, auto_filter, config):
        self.__auto_filter = auto_filter
        self.__ratio_counter = None
        self.__detector_corr = None
        self.__transmission_counter = None
        super().__init__(auto_filter.name, config, register_counters=False)

    def build_counters(self, config):
        self.__build_ratio_counter(config)
        self.__ref_transmission_counter()

    @property
    def inputs(self):
        mon = self.__auto_filter.monitor_counter
        self.tags[mon.name] = "monitor"
        det = self.__auto_filter.detector_counter
        self.tags[det.name] = "detector"
        transm = self.__transmission_counter
        self.tags[transm.name] = "transmission"
        self._input_counters = [mon, det, transm]
        return counter_namespace([mon, det, transm])

    @property
    def outputs(self):
        self.__build_detector_counter()
        if self.__detector_corr is None:
            counters = [self.__ratio_counter]
        else:
            counters = [self.__ratio_counter, self.__detector_corr]
        return counter_namespace(counters)

    def calc_function(self, input_dict):
        monitor_values = input_dict.get("monitor", [])
        detector_values = input_dict.get("detector", [])
        transmission_values = input_dict.get("transmission", [])
        detector_corr_name = self.tags[self.__detector_corr.name]
        detector_corr_values = detector_values / transmission_values
        ratio_name = self.tags[self.__ratio_counter.name]
        # use numpy divider to not get exception with division by zero
        # will result x/0 = Inf
        ratio_values = numpy.divide(detector_corr_values, monitor_values)

        return {ratio_name: ratio_values, detector_corr_name: detector_corr_values}

    def __build_ratio_counter(self, config):
        for counter_name, tag in self.__auto_filter.iter_counter_names(
            config, only_tags=["ratio"]
        ):
            cnt_ratio = AutoFilterCalcCounter(counter_name, self)
            self.tags[cnt_ratio.name] = tag
            self.__ratio_counter = cnt_ratio
            break
        else:
            raise RuntimeError(
                f"Ratio counter missing from configuration of {repr(self.__auto_filter.name)}"
            )

    def __ref_transmission_counter(self):
        for cnt in self.__auto_filter.filterset_counter_controller.counters:
            if cnt.tag == "transmission":
                self.__transmission_counter = cnt
                break
        else:
            raise RuntimeError("No transmission counter, cannot calculate correction")

    def __build_detector_counter(self):
        det_name = self.__auto_filter.detector_counter_name
        if not det_name:
            return
        det_name = det_name.split(":")[-1]
        corr_suffix = self.__auto_filter.corr_suffix
        det_corr = AutoFilterCalcCounter(f"{det_name}{corr_suffix}", self)
        self.tags[det_corr.name] = "detector_corr"
        self.__detector_corr = det_corr
