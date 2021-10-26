from pathlib import Path

"""
Requires "split -l 100000 file.csv" to be run first
Split files are output with a simple name convention: xaa.
the first 'x' represents the file was split.
The following letters represent a digits place. a = 1, z = 26
This code goes through all of those letters, and generates a number based upon a 'letter number' in the file name.
"""


def suffix_number(file_name: str) -> int:
    letter_values = []
    reverse_name = file_name[::-1]  # thanks stack overflow for this one.
    reverse_name = reverse_name[:-1]  # Strip the x from the name
    for index, value in enumerate(reverse_name):
        # For each letter passed the x in the file name
        # Take the ord of that value. ord(a) = 97, so ord(a) - 96 = 1
        # Add each of these values to a list, and then perform the math to return a single int value
        letter_values.append((ord(value) - 97) + (abs(index - 1) * 26))
    return sum(letter_values) - 26


can_data_files = Path().cwd()

split_file_prefix = "civic"
for each_file in can_data_files.iterdir():
    if "xa" in each_file.name:
        each_file.rename(f'{split_file_prefix}_{suffix_number(each_file.name)}.csv')



