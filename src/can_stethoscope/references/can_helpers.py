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


class CanVoltStats:
    def __init__(self, volts: pd.Series):
        self.volts = volts
        self.mean_expected = 2.5
        self.can_low_min = .3
        self.can_high_min = 1.7
        self.can_high_max = 3.3
        self.total_high_range = (self.can_high_max - self.can_high_min) / 2

        self.average = self._average_volt_high()

    def _average_volt_high(self) -> int:
        return self.volts[self.volts > self.can_low_min].median()

    def mean_stats(self):
        ratio = abs(self.mean_expected - self.average) / self.total_high_range
        average_ratio = round(ratio, 3)


