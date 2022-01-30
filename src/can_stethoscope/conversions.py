from typing import List
from can import Message
from references.can_helpers import CANBusType, BaudRates, Measurement


class ConvertVoltsToCAN:
    def __init__(self, baud_rate: BaudRates = BaudRates.bit_rate_250k):
        self.can_high_range = (3.9, 4.5)
        self.can_low_range = (.9, 1.5)
        self.baud_rate = baud_rate

    def voltage_to_byte_from_list(self,
                                  signal_data: List[Measurement],
                                  can_type: CANBusType) -> bytearray:
        """
        Takes in a list of signal data and converts it into a bytearray
        Todo: How to distinguish between multiple can messages in our data?
        :param can_type: Either CAN high or CAN low
        :param signal_data: list of voltages of a single CANbus line
        :return:
        """
        output_bytes: bytearray = bytearray()
        can_range = self.can_high_range if can_type == '1' else self.can_low_range
        start_timestamp = signal_data[0].timestamp
        return output_bytes

    def binary_to_can(self, input_bytearray: bytearray) -> Message:
        """
        From a byte representation of a CAN frame, returns a python-can message frame
        :param input_bytearray:
        :return:
        """
        output_message = Message()
        output_message.data = None
        return output_message


