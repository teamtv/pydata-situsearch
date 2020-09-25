from domain.models import Frame, TrackingDataset, ResultSet, Result

from .matchers import FrameMatcher


class SearchEngine:
    def __init__(self, matcher: FrameMatcher):
        self.matcher = matcher

    def search(self,
               query_frame: Frame,
               dataset: TrackingDataset,
               max_results: int = 100,
               min_score: float = 50) -> ResultSet:

        results = []
        for frame_to_score in dataset.frames:
            if frame_to_score == query_frame:
                continue

            score = self.matcher.match(
                query_frame,
                frame_to_score
            )

            if score < min_score:
                continue

            results.append(
                Result(
                    frame_id=frame_to_score.frame_id,
                    score=score
                )
            )

        results = sorted(results,
                         key=lambda result: result.score,
                         reverse=True)

        return ResultSet(results=results[:max_results])
