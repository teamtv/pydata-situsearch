import math

from scipy.spatial import distance
from munkres import munkres

from .base import ReferenceMatcher
from ... import Frame


def calculate_distance(X, Y):
    if not X and not Y:
        return 0
    cost = distance.cdist(X, Y)
    return cost[munkres(cost)].sum()


class MunkresMatcher(ReferenceMatcher):
    def match_frame(self, frame: Frame) -> float:
        ball_distance = math.sqrt(
            (frame.ball_coordinates.x - self.reference_frame.ball_coordinates.x) ** 2 +
            (frame.ball_coordinates.y - self.reference_frame.ball_coordinates.y) ** 2
        )

        home_players_distance = calculate_distance(
            [
                (player_coordinates.x, player_coordinates.y)
                for player_coordinates
                in frame.home_player_coordinates.values()
            ],
            [
                (player_coordinates.x, player_coordinates.y)
                for player_coordinates
                in self.reference_frame.home_player_coordinates.values()
            ],
        )

        away_players_distance = calculate_distance(
            [
                (player_coordinates.x, player_coordinates.y)
                for player_coordinates
                in frame.away_player_coordinates.values()
            ],
            [
                (player_coordinates.x, player_coordinates.y)
                for player_coordinates
                in self.reference_frame.away_player_coordinates.values()
            ],
        )

        frame_distance = ball_distance ** 2 / 2 + home_players_distance + away_players_distance

        return max(
            0,
            100 - (math.log2(frame_distance) if frame_distance > 1 else frame_distance)
        )
