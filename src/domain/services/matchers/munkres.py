import math

from scipy.spatial import distance
from munkres import munkres

from .base import FrameMatcher
from ... import Frame


def calculate_distance(X, Y):
    if not X and not Y:
        return 0
    cost = distance.cdist(X, Y)
    return cost[munkres(cost)].sum()


class MunkresMatcher(FrameMatcher):
    def match(self, frame1: Frame, frame2: Frame) -> int:
        ball_distance = math.sqrt(
            (frame1.ball_coordinates.x - frame2.ball_coordinates.x) ** 2 +
            (frame1.ball_coordinates.y - frame2.ball_coordinates.y) ** 2
        )

        home_players_distance = calculate_distance(
            [
                (player_coordinates.x, player_coordinates.y)
                for player_coordinates
                in frame1.home_player_coordinates
            ],
            [
                (player_coordinates.x, player_coordinates.y)
                for player_coordinates
                in frame1.home_player_coordinates
            ],
        )

        away_players_distance = calculate_distance(
            [
                (player_coordinates.x, player_coordinates.y)
                for player_coordinates
                in frame1.away_player_coordinates
            ],
            [
                (player_coordinates.x, player_coordinates.y)
                for player_coordinates
                in frame1.away_player_coordinates
            ],
        )

        return max(
            0,
            int(100 - (ball_distance ** 2 / 2 + home_players_distance + away_players_distance))
        )
