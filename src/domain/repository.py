from abc import abstractmethod, ABC

from domain import TrackingDataset


class Repository(ABC):
    @abstractmethod
    def load(self, dataset_id: str) -> TrackingDataset:
        pass

    @abstractmethod
    def save(self, dataset: TrackingDataset):
        pass
