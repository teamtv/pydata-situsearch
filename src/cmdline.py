import os, time
import sys
from contextlib import contextmanager

from application import SearchApplicationService
from domain import MunkresMatcher
from infrastructure import MetricaParser, LocalRepository, S3Repository


@contextmanager
def timeit(description: str):
    start = time.time()
    yield
    took = time.time() - start
    print(f"{description} took {took}")


if __name__ == "__main__":
    local_repository = LocalRepository("../data/processed")
    s3_repository = S3Repository("teamtv-pydata-demo")

    _, command = sys.argv
    if command == "fill-local-repository":
        parser = MetricaParser()
        data_dir = os.path.join(os.path.dirname(__file__), "../data/raw")
        with open(os.path.join(data_dir, "sample1_home.csv"), "r") as home, \
                open(os.path.join(data_dir, "sample1_away.csv"), "r") as away:
            with timeit("parse"):
                dataset = parser.parse(home.read(), away.read(), dataset_id="test")
        with timeit("write to local repository"):
            local_repository.save(dataset)
    elif command == "query-local-repository":
        search_service = SearchApplicationService(
            matcher_cls=MunkresMatcher,
            repository=local_repository
        )
        with timeit("search"):
            resultset = search_service.search_by_frame(
                "test", 201,
                min_score=0
            )
            print(f"Found {len(resultset.results)} results")

    elif command == "fill-s3-repository":
        parser = MetricaParser()
        data_dir = os.path.join(os.path.dirname(__file__), "../data/raw")
        with open(os.path.join(data_dir, "sample1_home.csv"), "r") as home, \
                open(os.path.join(data_dir, "sample1_away.csv"), "r") as away:
            with timeit("parse"):
                dataset = parser.parse(home.read(), away.read(), dataset_id="test")
        with timeit("write to s3 repository"):
            s3_repository.save(dataset)
    elif command == "search-s3-repository":
        search_service = SearchApplicationService(
            matcher_cls=MunkresMatcher,
            repository=s3_repository
        )
        with timeit("search"):
            resultset = search_service.search_by_frame(
                "test", 201,
                min_score=0
            )
            print(f"Found {len(resultset.results)} results")


