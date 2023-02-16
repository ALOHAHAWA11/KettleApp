import enum


class KettleState(enum.Enum):
    """Enum of a kettle's states"""
    POWER_ON = 1
    POWER_OFF = 2
    BOILED = 3
    STOPPED = 4

