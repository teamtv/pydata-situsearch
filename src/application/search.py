from typing import Type

from domain import SearchEngine, Repository, ResultSet, Matcher, ReferenceMatcher, Frame
from utils import timeit


class SearchService:
    def __init__(self, matcher_cls: Type[Matcher], repository: Repository):
        self.matcher_cls = matcher_cls
        self.repository = repository

    def get_frame_matcher(self, reference_frame: Frame) -> ReferenceMatcher:
        if not issubclass(self.matcher_cls, ReferenceMatcher):
            raise Exception("Provided match is not a reference matcher")
        return self.matcher_cls(reference_frame)

    def search_by_frame(self, dataset_id: str, reference_frame_id: int, **kwargs) -> ResultSet:
        dataset = self.repository.load(dataset_id)
        reference_frame = dataset.get_frame_by_id(reference_frame_id)

        with timeit(f"search {len(dataset.frames)} items"):
            return SearchEngine.search(
                dataset,
                matcher=self.get_frame_matcher(reference_frame),
                **kwargs
            )

    def search_by_matcher(self, dataset_id, matcher: Matcher) -> ResultSet:
        dataset = self.repository.load(dataset_id)
        return SearchEngine.search(
            dataset,
            matcher=matcher
        )
