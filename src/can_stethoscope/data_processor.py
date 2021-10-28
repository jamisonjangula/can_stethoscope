from src.can_stethoscope.file_manager import FileManager


class ProcessCanData:
    def __init__(self):
        self.file_manager = FileManager()

    @staticmethod
    def string_sci_to_float(input_string: str) -> float:
        """Converts an example string to int: ex = '-3.500000E-02' """
        magnitude = int(input_string[-2:])
        sign_string = input_string[-3:-2]
        main_value = float(input_string[1:-4])
        if sign_string == '-':
            return main_value * 10 ** (-magnitude)
        else:
            return main_value * 10 ** magnitude


    for each_file in can_data_files.iterdir():
        if each_file.glob('.csv'):
            with each_file.open() as input_stream:
                csv_reader = csv.DictReader(input_stream)
                file_data = [x for x in csv_reader]

            """
            At this point file_data contains the oscope data from Eric.
            Format is a list of dictionaries.
            keys are ordered:
            'Record Length', 'Analog:7000000', None
            First 11 lines are all metadata, and the rest are true voltage measurements
            """

            # Time_step: Convert the str into a float and find duration in nano seconds
            time_step_sec = float(file_data[0]['Analog:7000000'][3:]) * 100000000
            # True data starts 11 lines in and contains a weird mapping.
            # The third key is None, and its a list of a single value
            # Both values are casted as a string representation of scientific values

            can_high_data = [{"ch1": string_sci_to_float(x['Analog:7000000']),
                              "ch2": string_sci_to_float(x[None][0]),  # Oh.. oh no. This should not work... Yet it does
                              "timestamp": time_step_sec * string_sci_to_float(x['Record Length'])}
                             for x in file_data[11:]]


            with Path(each_file.name + '.json').open('w') as output_stream:
                json.dump(obj=can_high_data, fp=output_stream)
