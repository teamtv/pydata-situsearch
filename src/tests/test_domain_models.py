import pytest

from domain import Result


class TestDomainModels:

    def test_result_score(self):
        with pytest.raises(ValueError):
            Result(
                frame_id=1,
                score=-1
            )

        with pytest.raises(ValueError):
            Result(
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