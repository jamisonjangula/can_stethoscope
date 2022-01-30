from typing import List
from references.can_helpers import Measurement


class ScopeData:
    """
    Data storage object to manage processing the raw data
    Expected to convert the raw data generated from a SIGLENT sds1XXX model oscilloscope.
    Class requires initial list of metadata values.
    Additional lists of data can be added later.
    """

    def __init__(self, start_raw_data: List[List[str]]):
        if len(start_raw_data) < 12:
            raise ValueError("Data provided by oscope must contain at least 12 lines of metadata")

        if start_raw_data[1][0] != "Sample Interval":
            raise ValueError("Initial provided list does not contain correct metadata")

        self.model: str = start_raw_data[7][1]
        # This next conversion assumes the time-step is less then one second.
        self.time_step_nanosecond: float = float(start_raw_data[1][1].split('.')[1]) * 1000000000

        if len(start_raw_data) > 12:
            self.add_more_signals(start_raw_data[12:])

        self.signal_data: List[Measurement] = []
        self.total_data_duration: float

    def add_more_signals(self, more_signals: List[List[str]]):
        """Each line in the list is a list of each parameter"""
        for each_event in more_signals:
            # Contains three elements, time-step, ch1_v, ch2_v
            self.signal_data.append(self._process_event_line(each_event))

    def _process_event_line(self, line: List[str]) -> Measurement:
        live_measurement = Measurement()
        live_measurement.timestamp = self.str_to_float(line[0])
        live_measurement.chan_1_voltage = self.str_to_float(line[1])
        live_measurement.chan_2_voltage = self.str_to_float(line[2])
        return live_measurement

    @staticmethod
    def str_to_float(input_string: str) -> float:
        """Converts an example string to int: ex = '-3.500000E-02' """
        magnitude = int(input_string[-2:])
        sign_string = input_string[-3:-2]
        main_value = float(input_string[1:-4])
        if sign_string == '-':
            final_value = main_value * 10 ** (-magnitude)
        else:
            final_value = main_value * 10 ** magnitude
        return round(final_value, 9)
