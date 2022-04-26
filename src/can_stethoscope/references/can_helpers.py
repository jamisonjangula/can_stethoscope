import enum
from dataclasses import dataclass
import pandas as pd


class CANBusType(enum.Enum):
    CAN_LOW = 0
    CAN_HIGH = 1
    CAN_UNKNOWN = 2


class BaudRates:
    bit_rate_250k = 250000
    bit_rate_500k = 500000

    @staticmethod
    def time_diff(baud_rate) -> float:
        """Return time in seconds from baud rate"""
        return 1 / baud_rate


@dataclass
class Measurement:
    timestamp: float
    chan_1_voltage: float
    chan_2_voltage: float


@dataclass
class BinaryTimestamp:
    byte: CANBusType
    timestamp: float


@dataclass
class VoltageTimestamp:
    voltage: float
    timestamp: float


@dataclass
class PartialFrame:
    bit_stream: bytearray
    start_timestamp: float


class CanFrameStats:
    def __init__(self, single_frame: pd.DataFrame):
        self.volts = single_frame['volts']
        self.binary = single_frame['binary_filtered']
        self.mean_expected = 2.5
        self.can_low_min = .3
        self.can_high_min = 2.1
        self.can_high_max = 2.9
        self.total_high_range = (self.can_high_max - self.can_high_min) / 2

        self.average = self._average_volt_high()
        self.average_ratio = self._mean_stats()
        self.mode = self._mode_volt_high()

    def _average_volt_high(self) -> int:
        return self.volts[self.volts > self.can_low_min].median().round(decimals=3)

    def _mode_volt_high(self) -> int:
        return self.volts[self.volts > self.can_low_min].mode().round(decimals=3)

    def _mean_stats(self):
        ratio = abs(self.mean_expected - self.average) / self.total_high_range
        return round(ratio, 3)


class StatsCollector:
    def __init__(self):
        self.frames_stats = []
        self.averages = []
        self.modes = []
        self.ratios = []

    def add_frame(self, single_frame: pd.DataFrame):
        frame = CanFrameStats(single_frame)
        self.frames_stats.append(frame)
        self.averages.append(frame.average)
        self.modes.append(frame.mode)
        self.ratios.append(frame.average_ratio)





