from src.can_stethoscope.data_storage import ScopeData
from src.can_stethoscope.rise_time_analysis import rise_time_plot_data
import pandas


class ProcessCanData:
    def __init__(self, scope_data: ScopeData):
        self.scope_data = scope_data

    def basic_stats(self):
        """Read in the data from the scope_data storage object, and run basic analysis on it."""
        data_frame = pandas.DataFrame(self.scope_data.signal_data)
        print(data_frame.describe())

        rise_time_plot_data(self.scope_data.signal_data)

