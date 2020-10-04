from abc import ABC, abstractmethod

from domain import TrackingDataset


class Parser(ABC):
    @abstractmethod
    def parse(self, *args) -> TrackingDataset:
        pass