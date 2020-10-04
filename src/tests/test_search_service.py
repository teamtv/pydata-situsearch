import pytest

from application import SearchService
from domain import Repository, TrackingDataset, MunkresMatcher, Frame, Point, Result


class MemoryRepository(Repository):
    def __init__(self):
        self.items = {}

    def load(self, dataset_id: str) -> TrackingDataset:
        return self.items[dataset_id]

    def save(self, dataset: TrackingDataset):
        self.items[dataset.dataset_id] = dataset


class TestSearchService:
    def _init_search_service(self, repository=None):
        return SearchService(
            matcher_cls=MunkresMatcher,
            repository=repository if repository else MemoryRepository()
        )

    def test_unknown_frame(self):
        search_service = self._init_search_service()
        search_service.repository.save(
            TrackingDataset(
                dataset_id="test",
                frames=[]
            )
        )

        with pytest.raises(IndexError):
            search_service.search_by_frame("test", 1)

    def test_same_frame(self):
        repository = MemoryRepository()
        repository.save(
            TrackingDataset(
                dataset_id="test",
                frames=[
                    Frame(
                        frame_id=1,
                        timestamp=0,
                        ball_coordinates=Point(x=0, y=0),
                        home_player_coordinates=[],
                        away_player_coordinates=[]
                    )
                ]
            )
        )

        search_service = self._init_search_service(
            repository=repository
        )

        resultset = search_service.search_by_frame("test", 1)
        assert len(resultset.results) == 0

    def test_single_frame(self):
        search_service = self._init_search_service()
        search_service.repository.save(
            TrackingDataset(
                dataset_id="test",
                frames=[
                    Frame(
                        frame_id=1,
                        timestamp=0,
                        ball_coordinates=Point(x=0, y=0),
                        home_player_coordinates=[],
                        away_player_coordinates=[]
                    ),
                    Frame(
                        frame_id=2,
                        timestamp=0.1,
                        ball_coordinates=Point(x=1, y=0),
                        home_player_coordinates=[],
                        away_player_coordinates=[]
                    )
                ]
            )
        )

        resultset = search_service.search_by_frame("test", 1)
        assert resultset.results == [Result(frame_id=2, score=99)]
