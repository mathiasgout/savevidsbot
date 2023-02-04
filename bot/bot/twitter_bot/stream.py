from twitter_bot import logger, config
from twitter_bot.tools import twitter_tools
from twitter_bot.tools.error_tools import exception

import tweepy


class Streamer(tweepy.Stream):
    def __init__(self, settings: config.Settings, **kwargs):
        super().__init__(
            settings.TWITTER_API_KEY,
            settings.TWITTER_API_KEY_SECRET,
            settings.TWITTER_ACCESS_TOKEN,
            settings.TWITTER_ACCESS_TOKEN_SECRET,
            **kwargs,
        )
        self.settings = settings

    @exception(logger)
    def on_status(self, status):
        logger.info("Bot mentionned")
        twitter_tools.handle_new_status(settings=self.settings, status=status)

    def on_disconnect_message(self, message):
        logger.debug(f"Disconnect message : {message}")

    def on_limit(self, track):
        logger.warning(f"Limit notice : {track}")

    def on_warning(self, warning):
        logger.warning(f"Warning message : {warning}")

    def on_connect(self):
        logger.info("Connected")

    def on_connection_error(self):
        logger.error("Connection error")

    def on_closed(self, response):
        logger.error(f"Closed by Twitter : {response}")

    def on_disconnect(self):
        logger.info(f"Disconnected")

    def on_exception(self, exception):
        logger.error(f"Exception : {exception}")

    def on_request_error(self, status_code):
        logger.error(f"Request error : {status_code}")


@exception(logger)
def run_bot():
    settings = config.get_settings()
    streamer = Streamer(settings=settings)
    streamer.filter(track=[settings.TRACK])
