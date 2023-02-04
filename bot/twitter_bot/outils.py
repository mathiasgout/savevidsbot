from twitter_bot import logger
from db.firebase_db import edit_user_document, edit_video_document, get_document
from helpers.retry import retry
from helpers.logger import exception

import os
import datetime
from typing import Optional, Dict

import tweepy


class NewStatusHandler:
    def __init__(self, config) -> None:
        self.config = config

    @exception(logger)
    def handle_new_status(self, status: tweepy.models.Status) -> None:
        try:
            # Check if the tweet is a reply to another
            in_reply_to_status_id = self._get_in_reply_to_status_id(status)
            if in_reply_to_status_id:
                # Get the reply tweet and extract the video url from it (if it exits)
                in_reply_status = self._get_status(tweet_id=in_reply_to_status_id)
                urls = self._get_video_urls_from_status(status=in_reply_status)
                if urls:

                    # Check if its sensitive
                    if self._is_possibly_sensitive(status=in_reply_status):
                        logger.info(f"no reply sent, sensitive content")
                        return None

                    # Extract infos from tweet
                    tweet_info = self._extract_infos_from_status(status=status)
                    tweet_info_reply = self._extract_infos_from_status(
                        status=in_reply_status
                    )

                    # Check if the user is banned
                    if self._is_banned_user(user_id=str(tweet_info["user_id"])):
                        logger.info(f"no reply sent, banned user")
                        return None

                    # Udpate collection videos
                    asked_count = edit_video_document(
                        collection_name=self.config.VIDEOS_COLLECTION,
                        document_name=tweet_info_reply["tweet_id"],
                        video_url=urls["video_url"],
                        thumbnail_url=urls["thumbnail_url"],
                        tweet_id=tweet_info_reply["tweet_id"],
                        tweet_url=f'https://twitter.com/twitter/statuses/{tweet_info_reply["tweet_id"]}',
                        user_id=tweet_info_reply["user_id"],
                        screen_name=tweet_info_reply["screen_name"],
                        text=tweet_info_reply["text"],
                        asked_at=tweet_info_reply["asked_at"],
                    )

                    # Post status with url to download page if video was asked less than 6 times
                    if asked_count < 6:
                        text = f'{tweet_info["screen_name"]} Download link here! \n{os.path.join(self.config.URL_PREFIX, str(tweet_info_reply["tweet_id"]))}'
                        status_id = self._post_reply_status(
                            text=text, tweet_id=status.id
                        )
                    else:
                        logger.info(f"no reply sent, asked_count : {asked_count}")

                    # Udpate collection users
                    edit_user_document(
                        collection_name=self.config.USERS_COLLECTION,
                        document_name=tweet_info["screen_name"][1:],
                        requested_video={
                            "video_id": tweet_info_reply["tweet_id"],
                            "reply_tweet_id": str(status_id),
                        },
                        screen_name=tweet_info["screen_name"],
                        user_id=tweet_info["user_id"],
                    )

        except Exception as e:
            logger.error(f"Error occured : {e}")

    @exception(logger)
    def _get_twitter_api(self) -> tweepy.API:
        """Return Twitter API object
        Returns:
            tweepy.API: API twitter
        """

        auth = tweepy.OAuthHandler(
            self.config.TWITTER_API_KEY, self.config.TWITTER_API_KEY_SECRET
        )
        auth.set_access_token(
            self.config.TWITTER_ACCESS_TOKEN, self.config.TWITTER_ACCESS_TOKEN_SECRET
        )
        twitter_api = tweepy.API(auth, wait_on_rate_limit=True)

        return twitter_api

    @exception(logger)
    def _get_in_reply_to_status_id(self, status: tweepy.models.Status) -> Optional[int]:
        """Get in_reply_to_status_id from tweet status
        Args:
            tweet (tweepy.models.Status): a tweet status
        Returns:
            Optional[int]: in_reply_to_status_id or None if it doesnt exist
        """
        if status.in_reply_to_status_id:
            logger.debug("in_reply_to_status_id returned")
            return status.in_reply_to_status_id
        else:
            logger.debug("no in_reply_to_status_id found from tweet")
            return None

    @exception(logger)
    @retry(Exception, tries=3, delay=5, logger=logger)
    def _get_status(self, tweet_id: int) -> tweepy.models.Status:
        """Get a tweet status from a Tweet ID
        Args:
            tweet_id (int): tweet ID
        Returns:
            tweepy.models.Status: a tweet status, or None if tweet does not exist
        """
        twitter_api = self._get_twitter_api()
        status = twitter_api.get_status(id=tweet_id, tweet_mode="extended")
        logger.debug(f"tweet with id {tweet_id} found")
        return status

    @exception(logger)
    def _get_video_urls_from_status(
        self, status: tweepy.models.Status
    ) -> Dict[str, str]:
        """Get video url (video or gif) and video thumbnail from tweet
        Args:
            tweet (tweepy.models.Status): a tweet
        Returns:
            Dict[str, str]: {"video_url":video_url, "thumbnail_url":thumbnail_url}, or {} if no media in tweet
        """
        if not hasattr(status, "extended_entities"):
            logger.debug("no extended_entities in tweet")
            return {}

        media = status.extended_entities["media"][0]

        # Si c'est une vidéo
        if "video_info" in media:
            thumbnail_url = media["media_url_https"]
            variants = media["video_info"]["variants"]
            bitrate_url = {}
            for variant in variants:
                if ("bitrate" in variant) and ("url" in variant):
                    bitrate_url[variant["bitrate"]] = variant["url"]

            # Garde la vidéo de meilleure qualité
            if bitrate_url:
                logger.debug("video found in tweet status")
                return {
                    "video_url": bitrate_url[max(bitrate_url.keys())],
                    "thumbnail_url": thumbnail_url,
                }
        logger.debug("no video found in tweet status")
        return {}

    @exception(logger)
    def _extract_infos_from_status(self, status: tweepy.models.Status) -> Dict:
        """Extract informations from tweet status
        Args:
            tweet (tweepy.models.Status): a tweet status
        Returns:
            Dict: informations about the tweet status
        """
        tweet_info = {}
        tweet_info["tweet_id"] = str(status.id)
        tweet_info["user_id"] = str(status.user.id)
        tweet_info["screen_name"] = f"@{status.user.screen_name.lower()}"
        tweet_info["asked_at"] = int(
            datetime.datetime.timestamp(datetime.datetime.now())
        )
        if hasattr(status, "full_text"):
            text_split = status.full_text.split(" ")[:-1]
        else:
            text_split = status.text.split(" ")[:-1]
        tweet_info["text"] = " ".join(text_split)
        logger.debug(f"infos from status with id : {tweet_info['tweet_id']} extracted ")

        return tweet_info

    @exception(logger)
    def _is_possibly_sensitive(self, status: tweepy.models.Status) -> bool:
        """Check if status is possibly sensitive
        Args:
            status (tweepy.models.Status): a tweet status
        Returns:
            bool: True if it is possibly sensitive
        """
        is_sensitive = False
        if hasattr(status, "possibly_sensitive"):
            is_sensitive = status.possibly_sensitive
        return is_sensitive

    @exception(logger)
    def _is_banned_user(self, user_id: str) -> bool:
        banned_user = get_document(
            collection_name=self.config.BANNED_COLLECTION, document_name=user_id
        )
        if banned_user is not None:
            return True
        return False

    @exception(logger)
    @retry(Exception, tries=3, delay=5, logger=logger)
    def _post_reply_status(self, text: str, tweet_id: int) -> int:
        """Post tweet with url to the download page (in reply to tweet_id)
        Args:
            text (str): text with url to the download page
            tweet_id (int): tweet id to reply
        Returns:
            int: Reply Tweet ID
        """
        twitter_api = self._get_twitter_api()
        status = twitter_api.update_status(status=text, in_reply_to_status_id=tweet_id)
        status_id = status.id
        logger.info(f"Reply sent, reply Tweet ID: {status_id}")
        return status_id
