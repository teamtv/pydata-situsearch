from typing import Iterator

from domain import TrackingDataset, Frame, Point
from .base import Parser


class MetricaParser(Parser):
    @staticmethod
    def _create_point(x: str, y: str) -> Point:
        return Point(x=float(x) * 105, y=float(y) * 68)

    def parse(self, home_data: str, away_data: str, sample_rate=1/25, **kwargs) -> TrackingDataset:
        frames = []

        home_jersey_numbers = []
        away_jersey_numbers = []

        for line_idx, (home_line, away_line) in enumerate(zip(home_data.splitlines(keepends=False), away_data.splitlines(keepends=False))):
            if line_idx == 0 or line_idx == 2:
                continue

            home_period, home_frame_id, home_time, *home_players, home_ball_x, home_ball_y = home_line.split(",")
            away_period, away_frame_id, away_time, *away_players, away_ball_x, away_ball_y = away_line.split(",")

            if line_idx == 1:
                home_jersey_numbers = [int(number) for number in home_players[::2]]
                away_jersey_numbers = [int(number) for number in away_players[::2]]
                continue

            if home_frame_id != away_frame_id:
                raise Exception(f"Input file mismatch (frame_id): {home_frame_id} != {away_frame_id}")

            if home_ball_x != away_ball_x or home_ball_y != away_ball_y:
                raise Exception(f"Input file mismatch (ball): ({home_ball_x}, {home_ball_y}) != ({away_ball_x}, {away_ball_y})")

            if (line_idx - 3) % (1 / sample_rate) != 0:
                continue

            if home_ball_x == 'NaN' or away_ball_y == 'NaN':
                continue

            frame = Frame(
                frame_id=int(home_frame_id),
                timestamp=float(home_time),
                home_players_coordinates={
                    home_jersey_numbers[int(i / 2)]: self._create_point(
                        home_players[i],
                        home_players[i + 1]
                    )
                    for i in range(0, len(home_players), 2)
                    if home_players[i] != 'NaN'
                },
                away_players_coordinates={
                    away_jersey_numbers[int(i / 2)]: self._create_point(
                        away_players[i],
                        away_players[i + 1]
                    )
                    for i in range(0, len(away_players), 2)
                    if away_players[i] != 'NaN'
                },
                ball_coordinates=self._create_point(home_ball_x, away_ball_y)
            )
            frames.append(frame)

        return TrackingDataset(
            frames=frames,
            **kwargs
        )
