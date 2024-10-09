from enum import Enum
from lib.utils.cvss_vector import process_cvss_vector


class Severity(Enum):

    INFO = 1, "info"
    LOW = 2, "low"
    MEDIUM = 3, "medium"
    HIGH = 4, "high"
    CRITICAL = 5, "critical"

    def __new__(cls, *values):
        assert len(values) > 0
        obj = object.__new__(cls)
        obj._value_ = values[0]
        for other_value in values[1:]:
            cls._value2member_map_[other_value] = obj
        obj._all_values = values
        obj._cvss_score = None
        obj._cvss_vector = None
        return obj

    def __repr__(self):
        return "<%s.%s: %s>" % (
            self.__class__.__name__,
            self._name_,
            ", ".join([repr(v) for v in self._all_values]),
        )

    @staticmethod
    def from_cvss(cvss_score: float, cvss_vector: str):

        if cvss_score == 0.0:
            obj = Severity.INFO
        elif 0.0 < cvss_score < 4:
            obj = Severity.LOW
        elif 4 <= cvss_score < 7:
            obj = Severity.MEDIUM
        elif 7 < cvss_score < 9:
            obj = Severity.MEDIUM
        elif 9 <= cvss_score <= 10:
            obj = Severity.CRITICAL
        else:
            raise ValueError(f"Invalid CVSS score: {cvss_score}")
        obj._cvss_score = cvss_score
        if not isinstance(cvss_vector, list):
            if not isinstance(cvss_vector, str):
                raise ValueError(f"Invalid CVSS vector: {cvss_vector}")
            if "," in cvss_vector:
                cvss_vector = cvss_vector.split(",")
            elif "/" in cvss_vector:
                cvss_vector = cvss_vector.split("/")

        obj._cvss_vector = process_cvss_vector(cvss_vector)
        return obj

    @property
    def cvss_score(self):
        assert self._cvss_score is not None
        return self._cvss_score

    @property
    def cvss_vector(self):
        assert self._cvss_vector is not None
        return self._cvss_vector
