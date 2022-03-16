from can_stethoscope.data_storage import ScopeData
from can_stethoscope.conversions import ConvertMeasurements
from collections import OrderedDict

import pandas
import matplotlib.pyplot as plt


class ProcessCanData:
    def __init__(self, scope_data: ScopeData):
        self.scope_data = scope_data
        self.scope_data.sort_by_time_asc()
        self.processed_data = pandas.DataFrame()
        self.raw_data = pandas.DataFrame()
        self.populate_processed_data()

        self.binary_duration_map = []

    def plot_duration_periods(self):
        pass

    def generate_duration(self):
        """iterate through processed data and map timestamp and binary value to true timestamp"""
        start_time = self.processed_data.iloc[0]['time_filtered']
        start_value = self.processed_data.iloc[0]['binary_filtered']
        self.binary_duration_map = [{'start_time': start_time, "value": start_value, "duration": 0.0}]
        prev_value = 0
        for each_row in self.processed_data.iterrows():
            current_value = each_row[1]['binary_filtered']
            current_time = each_row[1]['time_filtered']
            if current_value != prev_value:
                self.binary_duration_map.append({'start_time': current_time, "value": current_value, "duration": 0.0})
                prev_value = current_value
            else:
                last_value_dict = self.binary_duration_map[-1]
                time_diff = current_time - last_value_dict['start_time']
                self.binary_duration_map[-1]['duration'] = round(time_diff, 13)

    def describe_and_plot_binary_duration(self):
        value_durations = pandas.DataFrame([x['duration'] for x in self.binary_duration_map])
        counts = value_durations.value_counts()
        counts.plot.bar()
        plt.show()

    def populate_processed_data(self):
        measurements = self.scope_data.signal_measurements
        volts_converter = ConvertMeasurements(measurements)
        volts_converter.measurements_to_binary_duration()
        self.raw_data["x_axis_time"] = [x.timestamp for x in measurements]
        self.raw_data["can_high"] = [x.chan_1_voltage for x in measurements]
        self.raw_data["can_low"] = [x.chan_2_voltage for x in measurements]
        self.raw_data["voltages"] = [x.voltage for x in volts_converter.voltage_list]
        self.raw_data["binary_list"] = [x.byte.value for x in volts_converter.binary_list]
        self.filter_binary()

    def filter_binary(self, filter_bin_value=8):
        binned_binary = self.raw_data['binary_list'].groupby(self.raw_data.index // filter_bin_value).median()
        binned_time = self.raw_data['x_axis_time'].groupby(self.raw_data.index // filter_bin_value).min()
        self.processed_data['time_filtered'] = binned_time
        self.processed_data['binary_filtered'] = binned_binary

    def basic_stats(self):
        """Read in the data from the scope_data storage object, and run basic analysis on it."""
        duration = self.raw_data['x_axis_time'][-1] - self.raw_data['x_axis_time'][0]
        print(f'Duration of sample: {duration}')
        data_frame = pandas.DataFrame(self.scope_data.signal_measurements)
        print(data_frame.describe())

    def histogram_plot(self):
        self.processed_data['binary_filtered'].plot()
        plt.show()

    def voltage_plot(self):
        self.filter_binary()
        self.raw_data["can_high"].plot()
        self.raw_data['can_low'].plot()
        self.raw_data['voltages'].plot()
        plt.show()

    def can_plot(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex='row')
        plot_frame = pandas.DataFrame()
        plot_frame['CAN data'] = self.processed_data['binary_filtered']
        plot_frame['voltages'] = self.raw_data['voltages'].groupby(self.processed_data.index // 20).mean()
        plot_frame['timestamp'] = self.processed_data['time_filtered']
        plot_frame.plot(x='timestamp', y='CAN data', kind='scatter', ax=ax1)
        plot_frame.plot(x='timestamp', y='voltages', kind='scatter', ax=ax2)
        plt.show()

