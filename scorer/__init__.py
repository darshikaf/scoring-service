from flask import Flask

from config import config, get_logger

_logger = get_logger(logger_name=__name__)

def create_app(config_name=None) -> Flask:
    """Create a flask app instance."""

    app = Flask("__name__")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # import blueprints
    from scorer.controller import prediction_app
    app.register_blueprint(prediction_app)

    _logger.debug('Application instance created')

    return app