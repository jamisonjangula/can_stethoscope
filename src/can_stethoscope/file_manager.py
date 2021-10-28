from pathlib import Path
from typing import List
import csv
import json


class FileManager:
    """
    Split files are output with a simple name convention: xaa.
    the first 'x' represents the file was split.
    The following letters represent a digits place. a = 1, z = 26
    This code goes through all of those letters, and generates a number based upon a 'letter number' in the file name.
    """
    def __init__(self):
        self.raw_data_location = Path('raw_can_data')
        # Todo: Create an interface class to communicate with user in CLI
        self.split_file_prefix = input("Please enter desired split file prefix: ")
        self.created_files: List[Path] = []

    @staticmethod
    def _suffix_number(file_name: str) -> int:
        # Todo: Create test for me! This was not trivial to make
        letter_values = []
        reverse_name = file_name[::-1]  # thanks stack overflow for this one.
        reverse_name = reverse_name[:-1]  # Strip the x from the name
        for index, value in enumerate(reverse_name):
            # For each letter passed the x in the file name
            # Take the ord of that value. ord(a) = 97, so ord(a) - 96 = 1
            # Add each of these values to a list, and then perform the math to return a single int value
            letter_values.append((ord(value) - 97) + (abs(index - 1) * 26))
        return sum(letter_values) - 26

    def process_raw(self):
        # Todo: Catch if user did not splice the correct file in the correct way.
        # Todo: Automate splice? - Risky
        for each_file in self.raw_data_location.iterdir():
            file_name: str = each_file.name
            if "xa" in file_name:
                each_file.rename(f'{self.split_file_prefix}_{self._suffix_number(file_name)}.csv')
                self.created_files.append(each_file)

    def get_raw_data(self) -> list:
        output_data = []
        for each_file in self.created_files:
            # Open each smaller file
            # Pull the CSV data and clean the data
            # Keep track of process
            pass
        return output_data
