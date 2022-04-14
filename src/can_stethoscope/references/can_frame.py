from typing import List, Literal
from dataclasses import dataclass


binary = Literal[0, 1]
dominate = Literal[0]
recessive = Literal[1]


@dataclass()
class PossibleFrame:
    binary_list: List[binary]
    start_time: int


class CanFrame:
    def __init__(self, frame: PossibleFrame):
        self.binary_list = frame.binary_list
        self.timestamp = frame.start_time

        self.minimum_binary_len = 52
        self.max_binary_len = 128

        if not self.minimum_binary_len < len(self.binary_list) < self.max_binary_len:
            raise ValueError('binary_list is incorrect length')

        self.start_of_frame: recessive = self.binary_list[0]
        self.can_id: List[binary] = self.binary_list[1:12]
        self.can_id_len = 11
        self.remote_request_bit: binary = self.binary_list[12]
        self.ide: dominate = self.binary_list[13]
        self.reserved_bit: dominate = self.binary_list[14]
        dlc_len = 4 + 15
        self.dlc: List[binary] = self.binary_list[15: dlc_len]
        data_end = dlc_len + self.gen_data_field_len()
        self.data_field: List[binary] = self.binary_list[dlc_len: data_end]
        crc_len = 15
        crc_end = crc_len + data_end
        self.crc: List[binary] = self.binary_list[data_end: crc_end]
        self.crc_delimiter: recessive = self.binary_list[crc_end: crc_end + 1][0]
        self.ack: binary = self.binary_list[crc_end + 1: crc_end + 2][0]
        self.ack_delimiter: recessive = self.binary_list[crc_end + 2: crc_end + 3][0]
        self.end_of_frame: List[recessive] = self.binary_list[crc_end + 3:]

    def __str__(self):
        output_str = f"\n" \
                     f"Timestamp: {self.timestamp}\n" \
                     f"ID: {self.list_to_hex(self.can_id)}\n" \
                     f"DLC: {self.list_to_hex(self.dlc)}\n" \
                     f"Data: {self.list_to_hex(self.data_field)}\n"
        return output_str

    @staticmethod
    def list_to_hex(values: list, bit_little_endian=True, byte_big_endian=True):
        if bit_little_endian:
            values.reverse()
        byte_len = 8
        hex_bits = []
        str_values = str(values).replace("[", "").replace(", ", "").replace(']', "")
        for length in range(0, len(values), 8):
            end = length + byte_len
            if end > len(values):
                end = len(values)
            hex_bits.append(str_values[length: end])
        if byte_big_endian:
            hex_bits.reverse()
        return [hex(int(x, 2)) for x in hex_bits]

    def gen_data_field_len(self):
        out = 0
        for bit in self.dlc:
            out = (out << 1) | bit
        if out >= 8:
            out = 8
        return out * 8

    def check_bits(self):
        """make a list of all the bit tests. Any False in the list shows a failure of the check"""
        bit_mapping_test = [self.binary_list[0] == 1,  # Sof bit
                            len(self.binary_list[1:12]) == self.can_id_len,  # can ID frame
                            ]

