import enum
import dataclasses


class CANBusType(enum.Enum):
    CAN_HIGH = "1"
    CAN_LOW = "2"


class BaudRates:
    bit_rate_250k = 250000
    bit_rate_500k = 500000

    def time_diff(self, baud_rate) -> float:
        """Return time in seconds from baud rate"""
        return 1 / baud_rate


class Measurement(dataclasses):
    timestamp: float
    chan_1_voltage: float
    chan_2_voltage: float

