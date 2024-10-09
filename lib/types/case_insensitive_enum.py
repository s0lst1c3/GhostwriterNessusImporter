from enum import Enum


class CaseInsensitiveEnum(Enum):

    @classmethod
    def _missing_(cls, value):
        if type(value) == str:

            value = value.upper()
            for member in cls:
                if member.name == value:
                    return member
        return None
