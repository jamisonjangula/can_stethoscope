import csv
from pathlib import Path
from typing import List
from can_stethoscope.data_storage import ScopeData


class FileManager:
    def __init__(self,
                 file_dir: str,
                 file_prefix: str = None):

        self.data_directory: str = file_dir
        self.raw_data_location: Path = None
        self._set_raw_data_dir()

        # Todo: Create an interface class to communicate with user in CLI
        self.file_prefix = file_prefix
        self.raw_data_suffix = "_raw_data.csv"
        self.created_files: List[Path] = []
        self.scope_data: ScopeData = None

    def _set_raw_data_dir(self):
        self.raw_data_location = Path(__file__).parent / self.data_directory
        if not self.raw_data_location.exists():
            raise FileNotFoundError(f'Unable to find directory at {self.raw_data_location}')

    @staticmethod
    def _suffix_number(file_name: str) -> int:
        letter_values = []
        reverse_name = file_name[::-1]  # Reverses the string
        reverse_name = reverse_name[:-1]  # Strip the x from the name
        for index, value in enumerate(reverse_name):
            # For each letter passed the x in the file name
            # Take the ord of that value. ord(a) = 97, so ord(a) - 96 = 1
            # Add each of these values to a list,
            # and then perform the math to return a single int value
            letter_values.append((ord(value) - 97) + (abs(index - 1) * 26))
        return sum(letter_values) - 26

    @staticmethod
    def open_csv(csv_file: Path) -> List[List[str]]:
        with csv_file.open() as input_stream:
            return [x for x in csv.reader(input_stream)]

    @staticmethod
    def _is_split_name(file_name: str) -> bool:
        """Checks if the provided name is a triple char string provided from a default linux split"""
        # Todo: Create test.csv!
        file_name.lower()
        if len(file_name) != 3:
            return False
        if not file_name[0] == 'x':
            return False
        char_state = [each_char.isalpha() for each_char in file_name[1:2]]
        return all(char_state)

    def _find_split_files(self) -> List[Path]:
        """Generates a list of Path's for any file in the raw_data directory which is the result of a split
        Split files are output with a simple name convention: xaa.
        the first 'x' represents the file was split.
        The following letters represent a digits place. a = 1, z = 26
        This code goes through all of those letters, and generates a number based upon a 'letter number'
        Additional reference about split: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/split.html
        """
        split_files = [each_file
                       for each_file in self.raw_data_location.iterdir()
                       if self._is_split_name(each_file.name)]
        return split_files

    def _find_block_files(self):
        found_csv_files = []
        for each_file in self.raw_data_location.iterdir():
            if '.csv' in each_file.name:
                found_csv_files.append(each_file)
        for each_found_file in found_csv_files:
            new_file_name = f'{self.file_prefix}_{each_found_file.stem}_raw_data.csv'
            new_file_path = self.raw_data_location / new_file_name
            each_found_file.rename(new_file_path)
            self.created_files.append(new_file_path)

    def _prefix_set(self) -> bool:
        """Check to see if prefix is set.
        Multiple different prefix may point to multiple subsets of data."""
        if self.file_prefix:
            return True

        found_prefix = []
        for each_file in self.raw_data_location.iterdir():
            file_name = each_file.name
            if self.raw_data_suffix in file_name:
                found_prefix.append(file_name.split("_")[0])

        found_prefix = list(set(found_prefix))
        if not found_prefix:
            return False
        elif len(found_prefix) > 1:
            raise FileNotFoundError(f"set prefix to one of: {found_prefix}")
        else:
            self.file_prefix = found_prefix[0]
            return True

    def _find_existing_files(self):
        if not self._prefix_set():
            # No processed files, lets search for raw files.
            return None
        for each_file in self.raw_data_location.iterdir():
            file_name = each_file.name
            if self.file_prefix in file_name and self.raw_data_suffix in file_name:
                self.created_files.append(each_file)
        self.created_files.sort()

    def _process_raw_filenames(self):
        """Formats split files"""
        if self.file_prefix is None:
            raise FileNotFoundError('set prefix')
        split_file_list = self._find_split_files()
        if split_file_list:
            for each_file in split_file_list:
                # If there are any split files, process them.
                file_name: str = each_file.name
                new_file_name = f'{self.file_prefix}_{self._suffix_number(file_name)}_raw_data.csv'
                new_file_path = self.raw_data_location / new_file_name
                each_file.rename(new_file_path)
                self.created_files.append(new_file_path)
        else:
            self._find_block_files()
        self.created_files.sort()

    def load_created_files(self):
        """Look through directory and find any data files"""
        try:
            self._find_existing_files()
            if self.created_files:
                # We found existing data, ignore trying to parse any raw data.
                return None
            self._process_raw_filenames()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"{e} in directory: {self.raw_data_location}")

    def _init_scope_data(self):
        """Generate the data storage class based upon metadata in spliced files"""
        # Now we have the files sorted by size, and we expect the first file to be 001.
        # This first file should have all the metadata in the first 12 lines.
        first_file = self.open_csv(self.created_files[0])
        metadata_list = first_file[:12]
        self.scope_data = ScopeData(metadata_list)
        self.scope_data.add_more_signals(first_file[12:])
        # At this point the first file transferred its metadata into the scope data, and any true data.
        self.created_files.pop(0)

    def _read_created_files(self):
        """Loads the raw data into the storage object"""
        for index, each_new_file in enumerate(self.created_files):
            file_data_list = self.open_csv(each_new_file)
            print(f"Reading file {index + 1} of {len(self.created_files)}", end='\r', flush=True)
            self.scope_data.add_more_signals(file_data_list)
        print("\n")

    def read_file_data(self):
        """Creates the data storage object, loads the raw data, and saves a clean set of data"""
        self.load_created_files()
        self._init_scope_data()
        self._read_created_files()
        print('done reading data')

