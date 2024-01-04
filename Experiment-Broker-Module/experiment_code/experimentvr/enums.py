from enum import Enum


class ParameterMapFailuremode(Enum):
    """Enum to arbitrate failure mode"""

    FailFast = True
    Continue = False
