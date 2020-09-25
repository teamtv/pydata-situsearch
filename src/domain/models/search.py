from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Result:
    frame_id: int
    score: int  # between 0 and 100


@dataclass(frozen=True)
class ResultSet:
    results: List[Result]


__all__ = [
    'Result',
    'ResultSet'
]
