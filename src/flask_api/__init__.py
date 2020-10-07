import os, sys

if 'DYNO' in os.environ:
    print("Add to path")
    sys.path.append(f'{os.path.dirname(__file__)}/build')


from flask import Flask, Response, jsonify, send_file
from flask_compress import Compress

from application import SearchApplicationService
from domain import MunkresMatcher
from infrastructure import S3Repository, LocalRepository
from infrastructure.serializers import DataSetToJson

#repository = S3Repository("teamtv-pydata-demo")
repository = LocalRepository(os.path.dirname(__file__) + "/../../data/processed")
search_service = SearchApplicationService(
    matcher_cls=MunkresMatcher,
    repository=repository
)

app = Flask('flask_app')
Compress(app)


def register_routes(app):
    @app.route("/datasets/<dataset_id>/search/<int:frame_id>")
    def search_frame(dataset_id: str, frame_id: int) -> Response:
        result_set = search_service.search_by_frame(dataset_id, frame_id)
        return jsonify(result_set.results)

    @app.route("/datasets/<dataset_id>/frames")
    def get_dataset(dataset_id: str) -> Response:
        dataset = repository.load(dataset_id)
        return Response(
            DataSetToJson.serialize(dataset),
            content_type="application/json"
        )

    @app.route("/")
    def index():
        return send_file(os.path.dirname(__file__) + "/index.html")


register_routes(app)
