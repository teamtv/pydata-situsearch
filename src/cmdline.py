import os, time
from contextlib import contextmanager

from application import SearchService
from domain import MunkresMatcher
from infrastructure import MetricaParser, LocalRepository, S3Repository


@contextmanager
def timeit(description: str):
    start = time.time()
    yield
    took = time.time() - start
    print(f"{description} took {took}")


if __name__ == "__main__":
    parser = MetricaParser()
    data_dir = os.path.join(os.path.dirname(__file__), "../data/raw")
    with open(os.path.join(data_dir, "sample1_home.csv"), "r") as home, \
            open(os.path.join(data_dir, "sample1_away.csv"), "r") as away:
        with timeit("parse"):
            dataset = parser.parse(home.read(), away.read(), dataset_id="test", sample_rate=1./12)

    # repository = S3Repository("teamtv-pydata-demo")

    repository = LocalRepository("../data/processed")
    repository.save(dataset)
    exit()
    # repository.save(dataset)

    search_service = SearchService(
        matcher_cls=MunkresMatcher,
        repository=repository
    )

    with timeit("search"):
        results = search_service.search_by_frame(
            "test", 201,
            min_score=0
        )

    a = 1
