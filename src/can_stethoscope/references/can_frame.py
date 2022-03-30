from typing import List, Literal


class CanFrame:
    def __init__(self, binary_list: list, timestamp: float):
        binary = Literal[0, 1]
        dominate = Literal[0]
        recessive = Literal[1]

        self.binary_list = binary_list
        self.timestamp = timestamp

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
        self.crc: binary = self.binary_list[data_end: crc_end]
        self.crc_delimiter: recessive = self.binary_list[crc_end: crc_end + 1]
        self.ack: binary = self.binary_list[crc_end + 1: crc_end + 2]
        self.ack_delimiter: recessive = self.binary_list[crc_end + 2: crc_end + 3]
        self.end_of_frame: List[recessive] = self.binary_list[crc_end + 3:]

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

