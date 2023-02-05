from twitter_bot.config import Settings


def override_get_settings():
    settings = Settings(
        ASKED_COUNT_MAX=5,
        ADMIN_USERNAME="admin_username",
        ADMIN_PASSWORD="admin_password",
        URL_PREFIX="/",
        API_PREFIX="http://0.0.0.0:8000/api/v2",
        TRACK="@testerbot806",
        TWITTER_API_KEY="twitter_api_key",
        TWITTER_API_KEY_SECRET="twitter_api_key_secret",
        TWITTER_ACCESS_TOKEN="twitter_access_token",
        TWITTER_ACCESS_TOKEN_SECRET="twitter_access_token_secret",
    )
    return settings
