from dataclasses import replace

import pytest

from domain import SearchEngine, MunkresMatcher, TrackingDataset, Frame, Point, Result


class TestSearchEngine:
    def test_empty_resultset(self):
        query_frame = Frame(
            frame_id=0,
            timestamp=0,
            ball_coordinates=Point(x=0, y=0),
            home_player_coordinates=[],
            away_player_coordinates=[]
        )

        dataset = TrackingDataset(
            dataset_id="test",
            frames=[]
        )

        resultset = SearchEngine.search(
            dataset,
            matcher=MunkresMatcher(query_frame)
        )

        assert len(resultset.results) == 0

    def test_same_frame(self):
        query_frame = Frame(
            frame_id=0,
            timestamp=0,
            ball_coordinates=Point(x=0, y=0),
            home_player_coordinates=[],
            away_player_coordinates=[]
        )

        dataset = TrackingDataset(
            dataset_id="test",
            frames=[query_frame]
        )

        resultset = SearchEngine.search(
            dataset,
            matcher=MunkresMatcher(query_frame)
        )

        assert len(resultset.results) == 0

    def test_single_match(self):
        query_frame = Frame(
            frame_id=0,
            timestamp=0,
            ball_coordinates=Point(x=0, y=0),
            home_player_coordinates=[],
            away_player_coordinates=[]
        )

        dataset = TrackingDataset(
            dataset_id="test",
            frames=[
                replace(
                    query_frame,
                    frame_id=1
                )
            ]
        )

        resultset = SearchEngine.search(
            dataset,
            matcher=MunkresMatcher(query_frame)
        )

        assert resultset.results == [Result(frame_id=1, score=100)]

    def test_min_score(self):
        query_frame = Frame(
            frame_id=0,
            timestamp=0,
            ball_coordinates=Point(x=0, y=0),
            home_player_coordinates=[],
            away_player_coordinates=[]
        )

        dataset = TrackingDataset(
            dataset_id="test",
            frames=[
                replace(
                    query_frame,
                    frame_id=1,
                    ball_coordinates=Point(x=0, y=100)
                ),
                replace(
                    query_frame,
                    frame_id=3
                )
            ]
        )

        resultset = SearchEngine.search(
            dataset,
            matcher=MunkresMatcher(query_frame)
        )

        assert resultset.results == [Result(frame_id=3, score=100)]

    def test_result_score(self):
        with pytest.raises(ValueError):
            score = Result(
                frame_id=1,
                score=-1
            )

        with pytest.raises(ValueError):
            score = Result(
                frame_id=1,
                score=101
            )

        result = Result(
            frame_id=1,
            score=0
        )
        assert result.score == 0

        result = Result(
            frame_id=1,
            score=100
        )
        assert result.score == 100