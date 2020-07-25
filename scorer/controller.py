from flask import Blueprint, request, jsonify
from regression_model.predict import make_prediction
from regression_model import __version__ as _version

from config import BASE_URL, get_logger
from scorer import __version__ as api_version

_logger = get_logger(logger_name=__name__)

prediction_app = Blueprint("prediction_app", __name__)


@prediction_app.route("/health", methods=["GET"])
def health():
    if request.method == "GET":
        _logger.info("health status OK")
        return "ok"


@prediction_app.route("/version", methods=["GET"])
def version():
    if request.method == "GET":
        return jsonify({"model_version": _version, "api_version": api_version})


@prediction_app.route(f"{BASE_URL}/score", methods=["POST"])
def predict():
    if request.method == "POST":
        json_data = request.get_json()
        _logger.info(f"Inputs: {json_data}")

        result = make_prediction(input_data=json_data)
        _logger.info(f"Outputs: {result}")

        predictions = result.get("predictions")[0]
        version = result.get("version")

        return jsonify({"predictions": predictions, "version": version})
