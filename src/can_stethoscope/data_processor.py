from data_storage import ScopeData


class ProcessCanData:
    def __init__(self, scope_data: ScopeData):
        self.scope_data = scope_data

    def convert_raw_data(self):
        raw_data: list = self.file_manager.get_clean_data()

        """
        At this point file_data contains the oscope data from Eric.
        Format is a list of dictionaries.
        keys are ordered:
        'Record Length', 'Analog:7000000', None
        First 11 lines are all metadata, and the rest are true voltage measurements
        """

        # Time_step: Convert the str into a float and find duration in nano seconds
        time_step_sec = float(raw_data[0]['Analog:7000000'][3:]) * 100000000
        # True data starts 11 lines in and contains a weird mapping.
        # The third key is None, and its a list of a single value
        # Both values are casted as a string representation of scientific values

        can_high_data = [{"ch1": self.string_sci_to_float(x['Analog:7000000']),
                          "ch2": self.string_sci_to_float(x[None][0]),  # Oh.. oh no. This should not work... Yet it does
                          "timestamp": time_step_sec * self.string_sci_to_float(x['Record Length'])}
                         for x in raw_data[11:]]

        self.file_manager.store_clean(can_high_data)
