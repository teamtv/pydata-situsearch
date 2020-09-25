from domain import Frame, Point, MunkresMatcher


class TestMunkresMatcher:
    def test_ball_distance(self):
        frame1 = Frame(
            frame_id=0,
            timestamp=10,
            home_player_coordinates=[],
            away_player_coordinates=[],
            ball_coordinates=Point(
                x=0,
                y=0
            )
        )

        frame2 = Frame(
            frame_id=0,
            timestamp=10,
            home_player_coordinates=[],
            away_player_coordinates=[],
            ball_coordinates=Point(
                x=0,
                y=0
            )
        )

        munkres_matcher = MunkresMatcher()
        score = munkres_matcher.match(frame1, frame2)
        assert score == 100

        frame3 = Frame(
            frame_id=0,
            timestamp=10,
            home_player_coordinates=[],
            away_player_coordinates=[],
            ball_coordinates=Point(
                x=0,
                y=1
            )
        )

        score = munkres_matcher.match(frame1, frame3)
        assert score == 99

        frame4 = Frame(
            frame_id=0,
            timestamp=10,
            home_player_coordinates=[],
            away_player_coordinates=[],
            ball_coordinates=Point(
                x=0,
                y=10
            )
        )

        score = munkres_matcher.match(frame1, frame4)
        assert score == 50

