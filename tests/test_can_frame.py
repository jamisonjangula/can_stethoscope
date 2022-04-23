from unittest import TestCase
from can_stethoscope.references.can_frame import CanFrame, PossibleFrame


class TestCanFrame(TestCase):
    def test_gen_data_field_len(self):
        temp_frame = PossibleFrame(binary_list=[1 for x in range(60)], start_time=0)
        can_frame = CanFrame(temp_frame, 1)
        expected_output = [0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 8, 8, 8]
        true_output = []
        data_set = []
        for value in range(0, 16):
            temp = []
            for bit in bin(value)[2:]:
                temp.append(int(bit))
            diff = 4 - len(temp)
            if diff > 0:
                for x in range(diff):
                    temp.insert(0, 0)
            data_set.append(temp)

        for each_value in data_set:
            can_frame.dlc = each_value
            true_output.append(can_frame.gen_data_field_len())

        self.assertEqual(expected_output, true_output)


