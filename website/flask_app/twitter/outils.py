from twitter import logger
from helpers.retry import retry
from helpers.logger import exception

import tweepy


class DeleteUserTweets:
    def __init__(self, config) -> None:
        self.config = config

    @exception(logger)
    def _get_twitter_api(self) -> tweepy.API:
        """Return Twitter API object
        Returns:
            tweepy.API: API twitter
        """

        auth = tweepy.OAuthHandler(
            self.config["TWITTER_API_KEY"], self.config["TWITTER_API_KEY_SECRET"]
        )
        auth.set_access_token(
            self.config["TWITTER_ACCESS_TOKEN"],
            self.config["TWITTER_ACCESS_TOKEN_SECRET"],
        )
        twitter_api = tweepy.API(auth, wait_on_rate_limit=True)

        return twitter_api

    @exception(logger)
    @retry(Exception, tries=3, delay=5, logger=logger)
    def delete_tweet(self, tweet_id: str):
        """Delete a tweet

        Args:
            tweet_id (str): tweet id
        """
        twitter_api = self._get_twitter_api()

        twitter_api.destroy_status(id=tweet_id)
        logger.info(f"Tweet with ID : {tweet_id} deleted")
