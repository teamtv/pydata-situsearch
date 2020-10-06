import boto3
import pickle

from domain import Repository, TrackingDataset


class S3Repository(Repository):
    def __init__(self, bucket_name: str):
        self.s3client = boto3.client("s3")
        self.bucket = boto3.resource("s3").Bucket(bucket_name)

    def load(self, dataset_id: str) -> TrackingDataset:
        response = self.s3client.get_object(Bucket=self.bucket.name, Key=f"{dataset_id}.pickle")
        return pickle.loads(response['Body'].read())

    def save(self, dataset: TrackingDataset):
        self.bucket.put_object(
            Key=f"{dataset.dataset_id}.pickle",
            Body=pickle.dumps(dataset)
        )
