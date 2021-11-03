from data_storage import ScopeData
import pandas


class ProcessCanData:
    def __init__(self, scope_data: ScopeData):
        self.scope_data = scope_data

    def basic_stats(self):
        """Read in the data from the scope_data storage object, and run basic analysis on it."""
        data_frame = pandas.DataFrame(self.scope_data.signal_data)
        print(data_frame.describe())

