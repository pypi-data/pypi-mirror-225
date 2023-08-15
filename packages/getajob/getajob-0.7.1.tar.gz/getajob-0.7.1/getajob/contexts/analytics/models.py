from enum import Enum


class TimeseriesGranularity(str, Enum):
    BUSINESS_DAY = "B"
    CALENDAR_DAY = "D"
    WEEKLY = "W"
    MONTHLY = "M"
    QUARTERLY = "Q"
    YEARLY = "A"
    HOURLY = "H"
    MINUTE = "T"
