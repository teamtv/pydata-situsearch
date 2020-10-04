from domain.models import TrackingDataset, ResultSet, Result

from .matchers import Matcher


class SearchEngine:
    @classmethod
    def search(self,
               dataset: TrackingDataset,
               matcher: Matcher,
               max_results: int = 100,
               min_score: float = 50) -> ResultSet:

        results = []
        for frame in dataset.frames:
            score = matcher.match(frame)

            if score < min_score:
                continue

            results.append(
                Result(
                    frame=frame,
                    score=score
                )
            )

        results = sorted(results,
                         key=lambda result: result.score,
                         reverse=True)

        return ResultSet(results=results[:max_results])
