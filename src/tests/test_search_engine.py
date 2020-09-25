from dataclasses import replace

from domain import SearchEngine, MunkresMatcher, TrackingDataset, Frame, Point, Result


class TestSearchEngine:
    def test_empty_resultset(self):
        search_engine = SearchEngine(
            matcher=MunkresMatcher()
        )

        query_frame = Frame(
            frame_id=0,
            timestamp=0,
            ball_coordinates=Point(x=0, y=0),
            home_player_coordinates=[],
            away_player_coordinates=[]
        )

        dataset = TrackingDataset(
            frames=[]
        )

        resultset = search_engine.search(query_frame, dataset)

        assert len(resultset.results) == 0

    def test_same_frame(self):
        search_engine = SearchEngine(
            matcher=MunkresMatcher()
        )

        query_frame = Frame(
            frame_id=0,
            timestamp=0,
            ball_coordinates=Point(x=0, y=0),
            home_player_coordinates=[],
            away_player_coordinates=[]
        )

        dataset = TrackingDataset(
            frames=[query_frame]
        )

        resultset = search_engine.search(query_frame, dataset)

        assert len(resultset.results) == 0

    def test_single_match(self):
        search_engine = SearchEngine(
            matcher=MunkresMatcher()
        )

        query_frame = Frame(
            frame_id=0,
            timestamp=0,
            ball_coordinates=Point(x=0, y=0),
            home_player_coordinates=[],
            away_player_coordinates=[]
        )

        dataset = TrackingDataset(
            frames=[
                replace(
                    query_frame,
                    frame_id=1
                )
            ]
        )

        resultset = search_engine.search(query_frame, dataset)

        assert resultset.results == [Result(frame_id=1, score=100)]


    def test_min_score(self):
        search_engine = SearchEngine(
            matcher=MunkresMatcher()
        )

        query_frame = Frame(
            frame_id=0,
            timestamp=0,
            ball_coordinates=Point(x=0, y=0),
            home_player_coordinates=[],
            away_player_coordinates=[]
        )

        dataset = TrackingDataset(
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

        resultset = search_engine.search(query_frame, dataset)

        assert resultset.results == [Result(frame_id=3, score=100)]

