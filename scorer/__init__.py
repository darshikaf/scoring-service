from flask import Flask

from config import config

def create_app(config_name=None) -> Flask:
    """Create a flask app instance."""

    app = Flask("__name__")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # import blueprints
    from scorer.controller import prediction_app
    app.register_blueprint(prediction_app)

    return app