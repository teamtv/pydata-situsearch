from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class Frame:
    frame_id: int
    timestamp: float
    home_player_coordinates: List[Point]
    away_player_coordinates: List[Point]
    ball_coordinates: Point


@dataclass(frozen=True)
class TrackingDataset:
    frames: List[Frame]


__all__ = [
    'TrackingDataset',
    'Frame',
    'Point'
]
