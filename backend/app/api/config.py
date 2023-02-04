from api import logger
from api.tools.error_tools import exception

import os
from configparser import ConfigParser
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Base config."""

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_KEY: str
    TWITTER_API_KEY: str
    TWITTER_API_KEY_SECRET: str
    TWITTER_ACCESS_TOKEN: str
    TWITTER_ACCESS_TOKEN_SECRET: str


# lru_cache pour par relire le fichier .env à chaque exécution de la fonction
@exception(logger)
@lru_cache()
def get_settings():
    """Returns the API settings

    Returns:
        Settings: the API settings
    """
    ENV_FILE_FOLDER = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    return Settings(_env_file=os.path.join(ENV_FILE_FOLDER, ".env"))


@lru_cache()
@exception(logger)
def get_db_config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db_config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_config[param[0]] = param[1]
    else:
        db_config["host"] = "host"
        db_config["port"] = 1
        db_config["database"] = "database"
        db_config["user"] = "user"
        db_config["password"] = "password"
    return db_config
