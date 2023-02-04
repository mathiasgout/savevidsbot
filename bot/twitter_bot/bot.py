from twitter_bot import logger
from twitter_bot.outils import NewStatusHandler
from helpers.logger import exception

import tweepy


class Streamer(tweepy.Stream):
    def __init__(self, config, **kwargs):
        super().__init__(
            config.TWITTER_API_KEY,
            config.TWITTER_API_KEY_SECRET,
            config.TWITTER_ACCESS_TOKEN,
            config.TWITTER_ACCESS_TOKEN_SECRET,
            **kwargs,
        )
        self.config = config

    @exception(logger)
    def on_status(self, status):
        logger.info("bot mentionned")
        handler = NewStatusHandler(config=self.config)
        handler.handle_new_status(status=status)

    def on_disconnect_message(self, message):
        logger.debug(f"disconnect message : {message}")

    def on_limit(self, track):
        logger.warning(f"limit notice : {track}")

    def on_warning(self, warning):
        logger.warning(f"warning message : {warning}")

    def on_connect(self):
        logger.info("connected")

    def on_connection_error(self):
        logger.error("connection error")

    def on_closed(self, response):
        logger.error(f"closed by Twitter : {response}")

    def on_disconnect(self):
        logger.info(f"disconnected")

    def on_exception(self, exception):
        logger.error(f"exception : {exception}")

    def on_request_error(self, status_code):
        logger.error(f"request error : {status_code}")


@exception(logger)
def run_bot(config):

    streamer = Streamer(config=config)

    streamer.filter(track=[config.TRACK])
