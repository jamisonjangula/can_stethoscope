from can_stethoscope.data_storage import ScopeData
from can_stethoscope.conversions import ConvertMeasurements
from can_stethoscope.references.can_frame import CanFrame, PossibleFrame

from typing import List
from pathlib import Path

import csv
import pandas
import numpy as np
import matplotlib.pyplot as plt


class ProcessCanData:
    def __init__(self, scope_data: ScopeData):
        # Bring in the scope data and sort it
        self.scope_data = scope_data
        self.scope_data.sort_by_time_asc()

        # set up data storage objects
        self.raw_data = pandas.DataFrame()
        self.processed_data = pandas.DataFrame()
        self.just_frames = []
        self.binary_message_list = pandas.Series(dtype='float64')
        self.converter_binary = None

        self.can_bit_stuffing = 6
        self.binary_duration_map = []
        self.minimum_binary_duration = None

        self.debugging = False

        # populate the raw and processed data objects.
        self._populate_processed_data()

    def _populate_processed_data(self):
        measurements = self.scope_data.signal_measurements
        volts_converter = ConvertMeasurements(measurements)
        volts_converter.measurements_to_binary_duration()
        self.converter_binary = pandas.DataFrame(volts_converter.binary_duration)
        self.raw_data["x_axis_time"] = [x.timestamp for x in measurements]
        self.raw_data["can_high"] = [x.chan_1_voltage for x in measurements]
        self.raw_data["can_low"] = [x.chan_2_voltage for x in measurements]
        self.raw_data["voltages"] = [x.voltage for x in volts_converter.voltage_list]
        self.raw_data["binary_list"] = [x.byte.value for x in volts_converter.binary_list]
        self.raw_data['binary_list'] = self.raw_data['binary_list'].replace(2, 1)
        self._filter_binary()

    def _filter_binary(self):
        filter_bin_value = 6
        binned_binary = self.raw_data['binary_list'].groupby(self.raw_data.index // filter_bin_value).median()
        binned_time = self.raw_data['x_axis_time'].groupby(self.raw_data.index // filter_bin_value).min()
        self.processed_data['time_filtered'] = binned_time
        self.processed_data['binary_filtered'] = binned_binary

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
        value_durations = pandas.DataFrame([x['duration'] for x in self.binary_duration_map])
        counts = value_durations.value_counts().sort_index()
        self.minimum_binary_duration = counts.idxmax()[0]

    def _generate_binary_messages(self):
        """Generate a dataframe of binary based upon minimum duration time"""
        min_time_value = self.processed_data['time_filtered'].min()
        self.processed_data['time_filtered'] = self.processed_data['time_filtered'] - min_time_value
        binary_frame = self.processed_data[['binary_filtered', 'time_filtered']].groupby(
            self.processed_data['time_filtered'] // self.minimum_binary_duration).median().set_index('time_filtered')
        binary_frame = binary_frame.rename({'binary_filtered': "binary_value"}, axis='columns')
        binary_frame['binary_value'] = binary_frame['binary_value'].apply(np.ceil)
        return binary_frame

    @staticmethod
    def _gen_values_map(binary_frame):
        """Generates a list of values, their sequential count, and the timestamp of the first detected value change"""
        value_count_map: List[dict] = [{"value": binary_frame.iloc[0]['binary_value'],
                                        "value_count": 1,
                                        "value_timestamp": binary_frame.iloc[0]}]
        for each_row in binary_frame.iterrows():
            prev_value = value_count_map[-1]['value']
            new_value = each_row[1]['binary_value']
            new_value = 1 if new_value > 0 else 0
            if new_value != prev_value:
                value_count_map.append({"value": new_value,
                                        "value_count": 1,
                                        "value_timestamp": each_row[0]})
            else:
                value_count_map[-1]['value_count'] += 1
        return value_count_map

    def _gen_possible_frames(self, value_count_map):
        """Run through the value map and generate a possible CAN frame from this data"""
        possible_frames: List[PossibleFrame] = []
        starting_frame = PossibleFrame(binary_list=[], start_time=0)
        possible_frames.append(starting_frame)
        new_frame_count = 0
        for each_value_count in value_count_map:
            value = each_value_count['value']
            value_count = each_value_count['value_count']
            timestamp = each_value_count['value_timestamp']
            last_frame: PossibleFrame = possible_frames[-1]
            if value_count <= self.can_bit_stuffing:
                # We found data that looks to be good. Let's add it
                last_frame.binary_list.extend([value for x in range(0, value_count)])
                last_frame.start_time = timestamp
            elif len(last_frame.binary_list) > 0:
                new_frame_count += 1
                # We don't want to append multiple empty frames, so we make sure the last frame was not empty.
                blank_frame = PossibleFrame(binary_list=[], start_time=0)
                possible_frames.append(blank_frame)
        return possible_frames

    def _generate_true_can_frames(self, possible_frames: List[PossibleFrame]) -> list:
        """Look through each possible frame and try to generate a can_frame"""
        can_frames: List[CanFrame] = []
        for each_frame in possible_frames:
            if not each_frame.binary_list:
                continue
            try:
                can_frames.append(CanFrame(each_frame, self.minimum_binary_duration))
            except ValueError as e:
                print(f'{e} {each_frame}')
        return can_frames

    def generate_can_msg_list(self) -> list:
        """generate binary data and try to get valid CAN_messages from it"""
        binary_frame = self._generate_binary_messages()
        value_count_map = self._gen_values_map(binary_frame)
        possible_frames = self._gen_possible_frames(value_count_map)
        can_messages = self._generate_true_can_frames(possible_frames)
        if self.debugging:
            binary_frame['x-axis'] = binary_frame.index
            binary_frame.plot.scatter(x='x-axis', y='binary_value')
            plt.show()
        return can_messages

    def can_to_csv(self, output_file: str):
        output = []
        data = self.generate_can_msg_list()
        for each_frame in data:
            output.append(each_frame.to_dict())
        with Path(f'{output_file}.csv').open('w') as output_stream:
            csv_writer = csv.DictWriter(fieldnames=output[0].keys(), f=output_stream)
            csv_writer.writeheader()
            csv_writer.writerows(output)

    def basic_stats(self):
        """Read in the data from the scope_data storage object, and run basic analysis on it."""
        duration = self.raw_data['x_axis_time'][-1] - self.raw_data['x_axis_time'][0]
        print(f'Duration of sample: {duration}')
        data_frame = pandas.DataFrame(self.scope_data.signal_measurements)
        print(data_frame.describe())

    def describe_and_plot_binary_duration(self):
        value_durations = pandas.DataFrame([x['duration'] for x in self.binary_duration_map])
        counts = value_durations.value_counts().sort_index()
        counts.plot.bar()
        plt.show()

    def _generate_just_binary(self):
        proc_data = self.processed_data[['binary_filtered', 'time_filtered']].set_index('time_filtered')
        for each_frame in self.generate_can_msg_list():
            data = proc_data.loc[each_frame.timestamp: each_frame.time_end]
            if data.empty:
                breakpoint()
            self.just_frames.append({'frame_data': data, "can_frame": each_frame})

    def plot_single_frame(self, index):
        self._generate_just_binary()
        single_frame = self.just_frames[index]
        fig, a = plt.subplots(1, 1)
        breakpoint()
        a.plot(single_frame['frame_data'])
        a.vlines(single_frame['can_frame'].times, 0, 1)
        a.set_xlabel('time since recording')
        a.set_title = str(single_frame['can_frame'])
        plt.show()

    def plot_binary(self):
        self.processed_data['binary_filtered'].plot()
        plt.show()

    def plot_raw_volts(self):
        self.raw_data["can_high"].plot()
        self.raw_data['can_low'].plot()
        self.raw_data['voltages'].plot()
        plt.show()

    def can_plot(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex='row')
        plot_frame = pandas.DataFrame()
        plot_frame['CAN data'] = self.processed_data['binary_filtered']
        plot_frame['voltages'] = self.raw_data['voltages'].groupby(self.processed_data.index // 8).mean()
        plot_frame['timestamp'] = self.processed_data['time_filtered']
        plot_frame.plot(x='timestamp', y='CAN data', kind='scatter', ax=ax1)
        plot_frame.plot(x='timestamp', y='voltages', kind='scatter', ax=ax2)
        plt.show()

