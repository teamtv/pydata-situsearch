import os
import pickle

from domain import Repository, TrackingDataset


class LocalRepository(Repository):
    serializer = pickle

    def __init__(self, base_dir: str):
        self.base_dir = base_dir

    def _get_filename(self, dataset_id: str) -> str:
        return f"{self.base_dir}/{os.path.basename(dataset_id)}.pickle"

    def load(self, dataset_id: str) -> TrackingDataset:
        with open(self._get_filename(dataset_id), "rb") as fp:
            return self.serializer.load(fp)

    def save(self, dataset: TrackingDataset):
        with open(self._get_filename(dataset.dataset_id), "wb") as fp:
            self.serializer.dump(dataset, fp)
