from typing import List, Union, Dict

from can_stethoscope.data_storage import ScopeData
from can_stethoscope.conversions import ConvertMeasurements

import pandas
import matplotlib.pyplot as plt


class ProcessCanData:
    def __init__(self, scope_data: ScopeData):
        self.scope_data = scope_data

    def basic_stats(self):
        """Read in the data from the scope_data storage object, and run basic analysis on it."""
        data_frame = pandas.DataFrame(self.scope_data.signal_measurements)
        print(data_frame.describe())

    def voltage_observation(self):
        measurements = self.scope_data.signal_measurements[1000: 3000]
        volts_converter = ConvertMeasurements(measurements)
        volts_converter.measurements_to_binary_duration()
        x_axis_time = [x.timestamp for x in measurements]
        can_high = [x.chan_1_voltage for x in measurements]
        can_low = [x.chan_2_voltage for x in measurements]
        voltages = [x.voltage for x in volts_converter.voltage_list]
        binary_list = [x.byte.value for x in volts_converter.binary_list]
        fig, (can_high_plt, can_low_plt, volt_plt, binary_plt) = plt.subplots(4, sharex=True)
        can_high_plt.plot(x_axis_time, can_high)
        can_low_plt.plot(x_axis_time, can_low)
        volt_plt.plot(x_axis_time, voltages)
        binary_plt.plot(x_axis_time, binary_list)
        plt.show()

    def _find_start_of_frame(self, binary_list: List[Dict[str, Union[float, bool]]]) -> float:
        """look at stream of binary and find start of frame bit."""
        timestamp_sof = 0.0
        for each_data_point in binary_list:
            pass
        return timestamp_sof

