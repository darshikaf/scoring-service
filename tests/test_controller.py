import json
import math

from regression_model.config import config as model_config
from regression_model.processing.data_management import load_dataset
from regression_model import __version__ as _version

def test_health_endpoint(test_client):
    response = test_client.get('/health')

    assert response.status_code == 200

def test_prediction_endpoint_returns_prediction(test_client):
    # Given
    # Load the test data from the regression_model package
    # This is important as it makes it harder for the test
    # data versions to get confused by not spreading it
    # across packages.
    test_data = load_dataset(file_name=model_config.TESTING_DATA_FILE)
    post_json = test_data[0:1].to_json(orient='records')

    # When
    response = test_client.post(f'/api/v1/predict',
                                      json=post_json)

    # Then
    assert response.status_code == 200
    response_json = json.loads(response.data)
    prediction = response_json['predictions']
    response_version = response_json['version']
    assert math.ceil(prediction) == 112476
    assert response_version == _version