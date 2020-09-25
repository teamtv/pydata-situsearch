from dataclasses import dataclass
from typing import List


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
