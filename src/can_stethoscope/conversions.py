from typing import List, Dict, Union
from can import Message
from can_stethoscope.references.can_helpers import BaudRates, Measurement


class ConvertVoltsToCAN:
    def __init__(self, baud_rate: BaudRates = BaudRates.bit_rate_250k):
        can_high_range = (3.9, 4.5)
        can_low_range = (.9, 1.5)
        self.can_signal_range = (can_high_range[0] - can_low_range[1]), (can_high_range[1] - can_low_range[0])
        self.baud_rate = baud_rate

    def _voltages_to_binary(self, ch_1_volt: float, ch_2_volt: float) -> bool:
        """Check if the difference between voltage ranges can be considered active."""
        volt_diff = abs(ch_1_volt - ch_2_volt)
        return self.can_signal_range[0] < volt_diff < self.can_signal_range[1]

    def _find_start_of_frame(self, binary_list: List[Dict[str, Union[float, bool]]]) -> float:
        """look at stream of binary and find start of frame bit."""
        timestamp_sof = 0.0
        for each_data_point in binary_list:
            pass
        return timestamp_sof

    def _binary_to_can(self, binary_list: List[Dict[str, Union[float, bool]]]) -> List[Message]:
        """From a byte representation of a CAN frame, returns a python-can message frame"""
        output_message = Message()
        output_message.data = None
        return [output_message]

    def measurements_to_can(self, signal_data: List[Measurement]):
        """Takes in a list of signal data and converts it into a list of binary values"""
        start_timestamp = signal_data[0].timestamp
        binary_list = [{"time_diff": x.timestamp - start_timestamp,
                        "bit": self._voltages_to_binary(x.chan_1_voltage, x.chan_2_voltage)}
                       for x in signal_data]
        data_by_duration = [{"value": binary_list[0]['bit'],
                             "duration": 0}]
        for each_event in binary_list:
            current_value = each_event['bit']
            if current_value == data_by_duration[-1]['value']:
                data_by_duration[-1]['duration'] += each_event['time_diff']
            else:
                data_by_duration.append({"value": current_value,
                                         "duration": 0})

        # Todo: Process the data_by_duration object to understand if any frames exist,
        #  and process any partial frames for additional measurement lists
        breakpoint()
