import logging
import os

basedir = os.path.abspath(os.path.dirname(__file__))

BASE_URL = "/scorer/api/v1/"

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get(
        "JWT_SECRET_KEY", "Sh... I am a Secret Key !"
    )

    JWT_TOKEN_EXPIRY_IN_SECS = os.environ.get(
        "JWT_TOKEN_EXPIRY_IN_SECS", 86400
    )

    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'data.db')}"  # TODO: change DB parameters

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {"production": ProductionConfig, "dev": DevConfig}