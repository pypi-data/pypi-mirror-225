from enum import Enum


class DataMonitorFraction(float, Enum):
    """Traffic light colours

    Added: GJB 25.4.22
    """

    GREEN = 1
    YELLOW = 2
    RED = 3


class PermittedTimeZones(str, Enum):
    TZ_LOCAL = "Europe/Oslo"
    TZ_NORDIC = "Europe/Oslo"
