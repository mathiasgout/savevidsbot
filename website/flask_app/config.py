import os

import dotenv

dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".env"))


class Config:
    """Base config."""

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SESSION_COOKIE_NAME = os.environ.get("SESSION_COOKIE_NAME")
    SESSION_COOKIE_SECURE = True
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    VIDEOS_PER_PAGE = 4


class ProdConfig(Config):
    ENV = "production"
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False
    VIDEOS_COLLECTION = "videos"
    USERS_COLLECTION = "users"
    BANNED_COLLECTION = "banned"
    AUTH_COLLECTION = "auth"
    TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY_PROD")
    TWITTER_API_KEY_SECRET = os.environ.get("TWITTER_API_KEY_SECRET_PROD")
    TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN_PROD")
    TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET_PROD")


class DevConfig(Config):
    ENV = "development"
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    VIDEOS_COLLECTION = "videos-dev"
    USERS_COLLECTION = "users-dev"
    BANNED_COLLECTION = "banned-dev"
    AUTH_COLLECTION = "auth-dev"
    TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY_DEV")
    TWITTER_API_KEY_SECRET = os.environ.get("TWITTER_API_KEY_SECRET_DEV")
    TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN_DEV")
    TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET_DEV")
