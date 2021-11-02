from pathlib import Path
from typing import List
from copy import copy
import csv
import json


class FileManager:
    """
    Split files are output with a simple name convention: xaa.
    the first 'x' represents the file was split.
    The following letters represent a digits place. a = 1, z = 26
    This code goes through all of those letters, and generates a number based upon a 'letter number' in the file name.
    """
    def __init__(self, split_file_name: str, clean_file_name: str):
        self.raw_data_location = Path('raw_can_data')
        # Todo: Create an interface class to communicate with user in CLI
        self.split_file_prefix = split_file_name
        self.clean_file_prefix = clean_file_name
        self.metadata: list
        self.created_files: List[Path] = []

    @staticmethod
    def _suffix_number(file_name: str) -> int:
        # Todo: Create test! This was not trivial to make
        letter_values = []
        reverse_name = file_name[::-1]  # thanks stack overflow for this one.
        reverse_name = reverse_name[:-1]  # Strip the x from the name
        for index, value in enumerate(reverse_name):
            # For each letter passed the x in the file name
            # Take the ord of that value. ord(a) = 97, so ord(a) - 96 = 1
            # Add each of these values to a list, and then perform the math to return a single int value
            letter_values.append((ord(value) - 97) + (abs(index - 1) * 26))
        return sum(letter_values) - 26

    def process_raw_filenames(self):
        # Todo: Catch if user did not splice the correct file in the correct way.
        # Todo: Automate splice? - Risky
        for each_file in self.raw_data_location.iterdir():
            file_name: str = each_file.name
            # Todo: Specify metadata file from first split file.
            if "xa" in file_name:
                new_file_string = f'{self.split_file_prefix}_{self._suffix_number(file_name)}.csv'
                each_file.rename(new_file_string)
                self.created_files.append(each_file)

    def read_created_files(self):
        # At this point we have a list of files we touched, and they should all be .csv now.
        # We have one last issue where the split likely blew away all of the csv required headers.
        # lets make our own.
        new_header: list = ["timestamp", "ch1_v", "ch2_v"]
        for each_new_file in self.created_files:
            with each_new_file.open() as input_stream:
                csv_reader = csv.reader(input_stream)
                temp_data = copy(new_header)
                for x in csv_reader:
                    temp_data.append(x)


    def get_clean_data(self) -> list:
        output_data = []
        for each_file in self.created_files:
            # Open each smaller file
            # Pull the CSV data and clean the data
            # Keep track of process

            # for each_file in can_data_files.iterdir():
            #     if each_file.glob('.csv'):
            #         with each_file.open() as input_stream:
            #             csv_reader = csv.DictReader(input_stream)
            #             file_data = [x for x in csv_reader]

            pass
        return output_data

    def store_clean(self, output_data: List):
        pass

