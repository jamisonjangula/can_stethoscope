import enum
from dataclasses import dataclass


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

