import os

import dotenv

dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".env"))


class ProdConfig:
    TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY_PROD")
    TWITTER_API_KEY_SECRET = os.environ.get("TWITTER_API_KEY_SECRET_PROD")
    TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN_PROD")
    TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET_PROD")
    TRACK = "@savevidsbot"
    VIDEOS_COLLECTION = "videos"
    USERS_COLLECTION = "users"
    BANNED_COLLECTION = "banned"
    URL_PREFIX = "https://savevidsbot.com/videos/"
    

class DevConfig:
    TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY_DEV")
    TWITTER_API_KEY_SECRET = os.environ.get("TWITTER_API_KEY_SECRET_DEV")
    TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN_DEV")
    TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET_DEV")
    TRACK = "@testerbot806"
    VIDEOS_COLLECTION = "videos-dev"
    USERS_COLLECTION = "users-dev"
    BANNED_COLLECTION = "banned-dev"
    URL_PREFIX = "/"