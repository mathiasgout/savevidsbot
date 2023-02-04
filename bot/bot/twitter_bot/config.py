import os
from dataclasses import dataclass
from functools import lru_cache

import dotenv


ENV_FILE_FOLDER = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
dotenv.load_dotenv(os.path.join(ENV_FILE_FOLDER, ".env"))


@dataclass
class Settings:
    """Base config"""

    ASKED_COUNT_MAX: int = 5
    URL_PREFIX: str = os.environ.get("URL_PREFIX")
    API_PREFIX: str = os.environ.get("API_PREFIX")
    TRACK: str = os.environ.get("TRACK")
    TWITTER_API_KEY: str = os.environ.get("TWITTER_API_KEY")
    TWITTER_API_KEY_SECRET: str = os.environ.get("TWITTER_API_KEY_SECRET")
    TWITTER_ACCESS_TOKEN: str = os.environ.get("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET: str = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")


@lru_cache()
def get_settings():
    """Returns the bot settings

    Returns:
        Settings: the bot settings
    """
    return Settings()
