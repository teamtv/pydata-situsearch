from dataclasses import dataclass
from typing import List, Dict


MARGIN = 10


@dataclass(frozen=True)
class Point:
    x: float  # in meters
    y: float  # in meters

    def __post_init__(self):
        if self.x < -MARGIN or self.x > 105 + MARGIN:
            raise ValueError("x must be between 0 and 105")

        if self.y < -MARGIN or self.y > 68 + MARGIN:
            raise ValueError("y must be between 0 and 68")


JerseyNumber = int


@dataclass(frozen=True)
class Frame:
    frame_id: int
    timestamp: float
    home_players_coordinates: Dict[JerseyNumber, Point]
    away_players_coordinates: Dict[JerseyNumber, Point]
    ball_coordinates: Point


@dataclass(frozen=True)
class TrackingDataset:
    dataset_id: str
    frames: List[Frame]

    def get_frame_by_id(self, frame_id) -> Frame:
        for frame in self.frames:
            if frame.frame_id == frame_id:
                return frame
        else:
            raise IndexError(f"Frame with id {frame_id} not found")


__all__ = [
    'TrackingDataset',
    'Frame',
    'Point'
]
