from typing import List, Union, Dict

from can_stethoscope.data_storage import ScopeData
from can_stethoscope.conversions import ConvertMeasurements

import pandas
import matplotlib.pyplot as plt


class ProcessCanData:
    def __init__(self, scope_data: ScopeData):
        self.scope_data = scope_data
        self.processed_data = pandas.DataFrame()
        self.populate_processed_data()

    def basic_stats(self):
        """Read in the data from the scope_data storage object, and run basic analysis on it."""
        data_frame = pandas.DataFrame(self.scope_data.signal_measurements)
        print(data_frame.describe())

    def populate_processed_data(self):
        measurements = self.scope_data.signal_measurements
        volts_converter = ConvertMeasurements(measurements)
        volts_converter.measurements_to_binary_duration()
        self.processed_data["x_axis_time"] = [x.timestamp for x in measurements]
        self.processed_data["can_high"] = [x.chan_1_voltage for x in measurements]
        self.processed_data["can_low"] = [x.chan_2_voltage for x in measurements]
        self.processed_data["voltages"] = [x.voltage for x in volts_converter.voltage_list]
        self.processed_data["binary_list"] = [x.byte.value for x in volts_converter.binary_list]

    def filter_binary(self, filter_bin_value=20):
        binned_binary = self.processed_data['binary_list'].groupby(self.processed_data.index // filter_bin_value).max()
        self.processed_data['binary_filtered'] = binned_binary

    def histogram_plot(self):
        self.processed_data['binary_filtered'].plot()
        plt.show()

    def voltage_plot(self):
        self.filter_binary()
        self.processed_data["can_high"].plot()
        self.processed_data['can_low'].plot()
        self.processed_data['voltages'].plot()
        plt.show()

    def can_plot(self):
        self.processed_data['binary_filtered'].plot(kind='bar')
        plt.show()

