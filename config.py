import logging
from logging.handlers import TimedRotatingFileHandler
import os
import pathlib
import sys

basedir = os.path.abspath(os.path.dirname(__file__))
PACKAGE_ROOT = pathlib.Path(basedir)

BASE_URL = "/api/v1/"

FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s —"
    "%(funcName)s:%(lineno)d — %(message)s"
)

LOG_DIR = PACKAGE_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "scorer.log"


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when="midnight")
    file_handler.setFormatter(FORMATTER)
    file_handler.setLevel(logging.WARNING)
    return file_handler


def get_logger(*, logger_name):
    """Get logger with prepared handlers."""

    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.INFO)

    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False

    return logger


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
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.join(basedir, 'data.db')}"
    )  # TODO: change DB parameters

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class TestingConfig(Config):
    TESTING = True


config = {
    "production": ProductionConfig,
    "dev": DevConfig,
    "test": TestingConfig,
}
