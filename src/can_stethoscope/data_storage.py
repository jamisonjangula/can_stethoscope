from typing import List
from can_stethoscope.references.can_helpers import Measurement


class ScopeData:
    """
    Data storage object to manage processing the raw data
    Expected to convert the raw data generated from a SIGLENT sds1XXX model oscilloscope.
    Class requires initial list of metadata values.
    Additional lists of data can be added later.
    """

    def __init__(self, start_raw_data: List[List[str]]):
        self.signal_measurements: List[Measurement] = []
        self.total_data_duration: float
        if len(start_raw_data) < 12:
            raise ValueError("Data provided by oscope must contain at least 12 lines of metadata")

        if start_raw_data[1][0] != "Sample Interval":
            raise ValueError("Initial provided list does not contain correct metadata")

        self.model: str = start_raw_data[7][1]
        # This next conversion assumes the time-step is less than one second.
        self.time_step_nanosecond: float = float(start_raw_data[1][1].split('.')[1]) * 1000000000

        if len(start_raw_data) > 12:
            self.add_more_signals(start_raw_data[12:])

    def add_more_signals(self, more_signals: List[List[str]]):
        """Each line in the list is a list of each parameter"""
        for each_event in more_signals:
            # Contains three elements, time-step, ch1_v, ch2_v
            self.signal_measurements.append(self._process_event_line(each_event))

    def _process_event_line(self, line: List[str]) -> Measurement:
        live_measurement = Measurement(timestamp=self.str_to_float(line[0]),
                                       chan_1_voltage=self.str_to_float(line[1]),
                                       chan_2_voltage=self.str_to_float(line[2]))
        return live_measurement

    def sort_by_time_asc(self):
        self.signal_measurements.sort(key=lambda x: x.timestamp)

    @staticmethod
    def str_to_float(input_string: str) -> float:
        """Converts an example string to float: ex = '-3.500000E-02'
        Strange issue: The data can have a negative value"""
        start_sign = input_string[0]
        input_string = input_string.lower()
        if "e" not in input_string:
            return round(float(input_string), 9)
        if start_sign in ['+', '-']:
            magnitude = int(input_string[-2:])
            sign_string = input_string[-3:-2]
            main_value = float(input_string[1:-4])
        else:
            magnitude = int(input_string[-2:])
            sign_string = input_string[-3:-2]
            main_value = float(input_string[:-4])

        if sign_string == '-':
            final_value = main_value * 10 ** (-magnitude)
        else:
            final_value = main_value * 10 ** magnitude
        if start_sign == "-":
            final_value = -final_value
        return round(final_value, 9)
