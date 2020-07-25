import json
import math

from regression_model.config import config as model_config
from regression_model.processing.data_management import load_dataset
from regression_model import __version__ as _version

from scorer import __version__ as api_version


def test_health_endpoint(test_client):
    response = test_client.get("/health")

    assert response.status_code == 200


def test_version_endpoint_returns_version(test_client):
    response = test_client.get("/version")

    assert response.status_code == 200

    response_json = json.loads(response.data)
    assert response_json["model_version"] == _version
    assert response_json["api_version"] == api_version


def test_prediction_endpoint_returns_prediction(test_client):
    test_data = load_dataset(file_name=model_config.TESTING_DATA_FILE)
    post_json = test_data[0:1].to_json(orient="records")

    response = test_client.post(f"/api/v1/score", json=post_json)

    assert response.status_code == 200
    response_json = json.loads(response.data)
    prediction = response_json["predictions"]
    response_version = response_json["version"]
    assert math.ceil(prediction) == 112476
    assert response_version == _version
