from api import logger, config
from api.tools.error_tools import exception, retry

from typing import Union

import tweepy


@exception(logger)
def get_twitter_api(settings: config.Settings) -> tweepy.API:
    """Get tweepy API instance

    Args:
        settings (config.Settings): app settings

    Returns:
        tweepy.API: tweepy api instance
    """
    auth = tweepy.OAuth1UserHandler(
        settings.TWITTER_API_KEY,
        settings.TWITTER_API_KEY_SECRET,
        settings.TWITTER_ACCESS_TOKEN,
        settings.TWITTER_ACCESS_TOKEN_SECRET,
    )
    twitter_api = tweepy.API(auth, wait_on_rate_limit=True)
    return twitter_api


@exception(logger)
@retry(Exception, tries=3, delay=2, logger=logger)
def delete_tweet(settings: config.Settings, tweet_id: str) -> Union[dict, None]:
    """Delete a tweet

    Args:
        settings (config.Settings): app settings
        tweet_id (str): tweet id

    Returns:
        dics: {"deleted_tweet_id": "deleted_tweet_id"}
    """
    twitter_api = get_twitter_api(settings=settings)
    twitter_api.destroy_status(id=tweet_id)
    logger.info(f"Tweet with ID : {tweet_id} deleted")
    return {"deleted_tweet_id": tweet_id}
