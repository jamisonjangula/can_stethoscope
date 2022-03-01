from typing import List, Dict

from can_stethoscope.references.can_helpers import BaudRates
from can_stethoscope.references.can_helpers import Measurement
from can_stethoscope.references.can_helpers import CANBusType
from can_stethoscope.references.can_helpers import BinaryTimestamp
from can_stethoscope.references.can_helpers import VoltageTimestamp


class ConvertMeasurements:
    def __init__(self, measurements: List[Measurement], baud_rate: BaudRates = BaudRates.bit_rate_250k):
        self.measurements = measurements
        self.measurements.sort(key=lambda x: x.timestamp)
        self.start_timestamp = self.measurements[0].timestamp
        self.voltage_list: List[VoltageTimestamp] = []
        self.binary_list: List[BinaryTimestamp] = []
        self.binary_duration: List[Dict] = []
        self.changing_volt_diff = .3, 1.75
        self.baud_rate = baud_rate

    def _volt_to_binary(self,
                        input_voltage: float,
                        threshold_min: float = None,
                        threshold_max: float = None) -> CANBusType:
        """from provided input voltage, returns boolean if value is less than min or greater than max
        Anything between these two values is considered to be an unknown state."""
        if threshold_min is None:
            threshold_min = self.changing_volt_diff[0]
        if threshold_max is None:
            threshold_max = self.changing_volt_diff[1]
        if input_voltage <= threshold_min:
            return CANBusType.CAN_LOW
        elif input_voltage >= threshold_max:
            return CANBusType.CAN_HIGH
        else:
            return CANBusType.CAN_UNKNOWN

    def _generate_binary_list(self):
        """Iterate through measurements and populate the binary list of BinaryTimestamp objects"""
        for each_measure in self.measurements:
            volt_diff = abs(each_measure.chan_1_voltage - each_measure.chan_2_voltage)
            time_diff = each_measure.timestamp - self.start_timestamp
            binary_timestamp = BinaryTimestamp(byte=self._volt_to_binary(input_voltage=volt_diff),
                                               timestamp=time_diff)
            self.binary_list.append(binary_timestamp)
            volt_timestamp = VoltageTimestamp(voltage=volt_diff,
                                              timestamp=time_diff)
            self.voltage_list.append(volt_timestamp)

    def measurements_to_binary_duration(self):
        """
        The conversion class is created with a list of measurement objects that contain raw voltages and a timestamp
        this function goes through and converts the measurements into a best-guess detection of a binary value.

        From a stream of binary timestamps, we reduce this list into an ordered list of binary values,
        their start times, and their duration.
        :return:
        """
        self._generate_binary_list()
        self.binary_duration = [{"start_timestamp": self.binary_list[0].timestamp,
                                 "byte": self.binary_list[0].byte}]
        for each_event in self.binary_list:
            last_value: CANBusType = self.binary_duration[-1]['byte']
            last_start_time = self.binary_duration[-1]['start_timestamp']
            new_value = each_event.byte
            new_start_time = each_event.timestamp
            if new_value != last_value:
                old_duration = new_start_time - last_start_time
                self.binary_duration[-1]['duration'] = old_duration
                self.binary_duration.append({"start_timestamp": new_start_time,
                                             "byte": new_value})
        else:
            old_duration = new_start_time - last_start_time
            self.binary_duration[-1]['duration'] = old_duration





