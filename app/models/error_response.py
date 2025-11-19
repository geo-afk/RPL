from dataclasses import dataclass
from enum import IntEnum

class MarkerSeverity(IntEnum):
    Error = 8
    Warning = 4
    Info = 2
    Hint = 1


@dataclass
class ErrorResponse:
    error_code: MarkerSeverity
    column_number: int
    line_number: int
    message: str
