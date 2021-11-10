import csv
from pathlib import Path
from typing import List
from can_stethoscope.data_storage import ScopeData


class FileManager:
    """
    Split files are output with a simple name convention: xaa.
    the first 'x' represents the file was split.
    The following letters represent a digits place. a = 1, z = 26
    This code goes through all of those letters, and generates a number based upon a 'letter number' in the file name.
    Additional reference about split: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/split.html
    """
    def __init__(self, split_file_name: str, clean_file_name: str):
        self.raw_data_location = Path(__file__).parent / 'raw_can_data'
        # Todo: Create an interface class to communicate with user in CLI
        self.split_file_prefix = split_file_name
        self.raw_data_suffix = "_raw_data.csv"
        self.clean_file_prefix = clean_file_name
        self.created_files: List[Path] = []
        self.scope_data: ScopeData = None

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

    @staticmethod
    def open_csv(csv_file: Path) -> List[List[str]]:
        with csv_file.open() as input_stream:
            csv_reader = csv.reader(input_stream)
            output_data = [x for x in csv_reader]
            return output_data

    @staticmethod
    def _is_split_name(file_name: str) -> bool:
        """Checks if the provided name is a triple char string provided from a default linux split"""
        # Todo: Create test!
        file_name.lower()
        if len(file_name) != 3:
            return False
        if not file_name[0] == 'x':
            return False
        char_state = [each_char.isalpha() for each_char in file_name[1:2]]
        return all(char_state)

    def _find_split_files(self) -> List[Path]:
        """Generates a list of Path's for any file in the raw_data directory which is the result of a split"""
        return [each_file for each_file in self.raw_data_location.iterdir() if self._is_split_name(each_file.name)]

    def _find_existing_data(self) -> List[Path]:
        found_files: List[Path] = []
        for each_file in self.raw_data_location.iterdir():
            file_name = each_file.name
            if self.split_file_prefix in file_name and self.raw_data_suffix in file_name:
                found_files.append(each_file)
        return found_files

    def process_raw_filenames(self):
        """Formats split files, creates the data storage object, loads the raw data, and saves a clean set of data"""
        split_file_list = self._find_split_files()
        if not len(split_file_list):
            existing_data = self._find_existing_data()
            if not existing_data:
                raise FileNotFoundError("Unable to find any split or existing data"
                                        f" in directory: {self.raw_data_location}")
            self.created_files.extend(existing_data)
        for each_file in split_file_list:
            file_name: str = each_file.name
            new_file_name = f'{self.split_file_prefix}_{self._suffix_number(file_name)}_raw_data.csv'
            new_file_path = Path(self.raw_data_location / new_file_name)
            each_file.rename(new_file_path)
            self.created_files.append(new_file_path)
        self.created_files.sort()
        self.init_scope_data()
        self.read_created_files()
        self.save_clean_data()

    def init_scope_data(self):
        """Generate the data storage class based upon metadata in spliced files"""
        # Now we have the files sorted by size, and we expect the first file to be 001.
        # This first file should have all the metadata in the first 12 lines.
        metadata_list = self.open_csv(self.created_files[0])[:12]
        self.scope_data = ScopeData(metadata_list)
        # At this point the first file transferred its metadata into the scope data, and any true data.
        self.created_files.pop(0)

    def read_created_files(self):
        """Loads the raw data into the storage object"""
        for index, each_new_file in enumerate(self.created_files):
            file_data_list = self.open_csv(each_new_file)
            print(f"Reading file {index} of {len(self.created_files)}", end='\r', flush=True)
            self.scope_data.add_more_signals(file_data_list)

    def save_clean_data(self):
        clean_file_name = f"{self.clean_file_prefix}_{self.scope_data.model}_data.csv"
        clean_data_path = Path(self.raw_data_location / clean_file_name)
        with clean_data_path.open('w') as output_stream:
            csv_writer = csv.DictWriter(fieldnames=self.scope_data.fieldnames, f=output_stream)
            csv_writer.writeheader()
            csv_writer.writerows(self.scope_data.signal_data)

