from lib.types.case_insensitive_enum import CaseInsensitiveEnum


class FindingType(CaseInsensitiveEnum):

    NETWORK = 1
    PHYSICAL = 2
    WIRELESS = 3
    WEB = 4
    MOBILE = 5
    CLOUD = 6
    HOST = 7
