from abc import abstractmethod, ABC

from domain import Frame


class FrameMatcher(ABC):
    @abstractmethod
    def match(self, frame1: Frame, frame2: Frame) -> int:
        pass
