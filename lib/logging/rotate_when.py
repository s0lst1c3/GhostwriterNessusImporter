from lib.types.case_insensitive_enum import CaseInsensitiveEnum


class RotateWhen(CaseInsensitiveEnum):

    SECONDS = "S"
    MINUTES = "M"
    HOURS = "H"
    DAYS = "D"
    SUNDAY = "W0"
    MONDAY = "W1"
    TUESDAY = "W2"
    WEDNESDAY = "W3"
    THURSDAY = "W4"
    FRIDAY = "W5"
    SATURDAY = "W6"
    MIDNIGHT = "midnight"
