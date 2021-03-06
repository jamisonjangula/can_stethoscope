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
    def __init__(self, frame: PossibleFrame, bit_len):
        self.binary_list = frame.binary_list
        self.timestamp = frame.start_time

        self.minimum_binary_len = 52
        self.max_binary_len = 128

        can_id_len = 11
        dlc_len = 4 + 15
        self.dlc: List[binary] = self.binary_list[15: dlc_len]
        data_end = dlc_len + self.gen_data_field_len()
        bit_position_after_data = data_end + 17
        crc_len = 15
        crc_end = crc_len + data_end
        frame_end = crc_end + 3

        if frame_end > len(self.binary_list):
            raise ValueError(f'binary_list incorrect length. Should be {frame_end}, '
                             f'{len(self.binary_list)} given')

        self.start_of_frame: recessive = self.binary_list[0]

        self.can_id: List[binary] = self.binary_list[1: can_id_len]
        self.remote_request_bit: binary = self.binary_list[can_id_len + 1]
        self.ide: dominate = self.binary_list[can_id_len + 2]
        self.reserved_bit: dominate = self.binary_list[can_id_len + 3]

        self.data_field: List[binary] = self.binary_list[dlc_len: data_end]
        self.crc: List[binary] = self.binary_list[data_end: crc_end]

        self.crc_delimiter: recessive = self.binary_list[crc_end: crc_end + 1][0]
        self.ack: binary = self.binary_list[crc_end + 1: crc_end + 2][0]
        self.ack_delimiter: recessive = self.binary_list[crc_end + 2: frame_end][0]

        self.end_of_frame: List[recessive] = self.binary_list[frame_end:]

        time_can_id = self.timestamp + bit_len
        time_dlc = self.timestamp + bit_len * 15
        time_dlc_start = self.timestamp + bit_len * dlc_len
        time_dlc_end = self.timestamp + bit_len * data_end
        self.time_crc_end = self.timestamp + bit_len * crc_end
        self.time_end = self.timestamp + bit_len * (len(self.binary_list) + 7)

        self.times = [time_can_id, time_dlc, time_dlc_end, time_dlc_start, self.time_end]
        self.every_sample = [self.timestamp + x * bit_len for x in range(len(self.binary_list))]

    def __str__(self):
        output_str = f"\n" \
                     f"Timestamp: {self.timestamp}\n" \
                     f"ID: {self.list_to_hex(self.can_id)}\n" \
                     f"DLC: {self.list_to_hex(self.dlc)}\n" \
                     f"Data: {self.list_to_hex(self.data_field)}\n"
        return output_str

    def print_title(self):
        return f"ID:{self.list_to_hex(self.can_id)} DLC:{self.list_to_hex(self.dlc)} Data:{self.list_to_hex(self.data_field)}"

    def to_dict(self):
        output_dict = {"Timestamp": self.timestamp,
                       "ID": self.list_to_hex(self.can_id),
                       "DLC": self.list_to_hex(self.dlc),
                       "Data": self.list_to_hex(self.data_field)}
        return output_dict

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
        """returns number of bytes"""
        out = 0
        for bit in self.dlc:
            out = (out << 1) | bit
        if out >= 8:
            out = 8
        return out * 8
