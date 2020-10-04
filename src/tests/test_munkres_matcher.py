from domain import Frame, Point, MunkresMatcher


class TestMunkresMatcher:
    def test_ball_distance(self):
        frame1 = Frame(
            frame_id=0,
            timestamp=10,
            home_player_coordinates={},
            away_player_coordinates={},
            ball_coordinates=Point(
                x=0,
                y=0
            )
        )

        frame2 = Frame(
            frame_id=1,
            timestamp=10,
            home_player_coordinates={},
            away_player_coordinates={},
            ball_coordinates=Point(
                x=0,
                y=0
            )
        )

        munkres_matcher = MunkresMatcher(
            reference_frame=frame1
        )
        score = munkres_matcher.match(frame2)
        assert score == 100

        frame3 = Frame(
            frame_id=0,
            timestamp=10,
            home_player_coordinates={},
            away_player_coordinates={},
            ball_coordinates=Point(
                x=0,
                y=1
            )
        )

        score = munkres_matcher.match(frame3)
        assert score == 99.5

        frame4 = Frame(
            frame_id=0,
            timestamp=10,
            home_player_coordinates={},
            away_player_coordinates={},
            ball_coordinates=Point(
                x=0,
                y=10
            )
        )

        score = munkres_matcher.match(frame4)
        assert score == 94.35614381022528

