from typing import List


class ScopeData:
    """
    Data storage object to manage processing the raw data
    Expected to convert the raw data generated from a SIGLENT sds1XXX model oscilloscope.
    Class requires initial list of metadata values.
    Additional lists of data can be added later.
    """
    def __init__(self, start_raw_data: List[str]):
        if len(start_raw_data) <= 12:
            raise ValueError("Data provided by oscope must contain at least 12 lines of metadata")

        if "Sample Interval" not in start_raw_data[1]:
            raise ValueError("Initial provided list does not contain metadata")

        if len(start_raw_data) > 12:
            self.raw_data = start_raw_data
        else:
            self.raw_data = []

        self.model: str = start_raw_data[7].split(',')[1]
        # This next conversion assumes the time-step is less then one second.
        self.time_step_nanosecond: float = float(start_raw_data[1].split('.')[1]) * 1000000000

        self.signal_data: List[dict]
        self.total_data_duration: float

    def add_more_signals(self, more_signals: List[str]):
        for each_event in more_signals:
            pass

    def _process_event_line(self, line: dict) -> dict:
        output_dict = {"timestamp": line,
                       "ch1_v": line}
        return output_dict

    @staticmethod
    def string_sci_to_float(input_string: str) -> float:
        """Converts an example string to int: ex = '-3.500000E-02' """
        magnitude = int(input_string[-2:])
        sign_string = input_string[-3:-2]
        main_value = float(input_string[1:-4])
        if sign_string == '-':
            return main_value * 10 ** (-magnitude)
        else:
            return main_value * 10 ** magnitude








