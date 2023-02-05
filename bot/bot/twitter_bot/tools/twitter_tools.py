from twitter_bot import logger, config, schemas
from twitter_bot.tools import basic_tools, api_tools
from twitter_bot.tools.error_tools import exception, retry

import os
from typing import Union

import tweepy


@exception(logger)
def get_twitter_api(settings: config.Settings) -> tweepy.API:
    """Get tweepy API instance

    Args:
        settings (config.Settings): bot settings

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
@retry(Exception, tries=3, delay=3, logger=logger)
def get_status(
    settings: config.Settings, tweet_id: Union[str, int]
) -> tweepy.models.Status:
    """Get a tweet status from a Tweet ID

    Args:
        tweet_id (Union[str, int]): tweet ID

    Returns:
        tweepy.models.Status: a tweet status
    """
    twitter_api = get_twitter_api(settings=settings)
    status = twitter_api.get_status(id=str(tweet_id), tweet_mode="extended")
    logger.info(f"Status with ID : '{tweet_id}' found")
    return status


@exception(logger)
def get_in_reply_to_status_id(status: tweepy.models.Status) -> Union[int, None]:
    """Get in_reply_to_status_id from tweet status

    Args:
        tweet (tweepy.models.Status): a tweet status

    Returns:
        Union[int, None]: in_reply_to_status_id or None if it doesnt exist
    """
    if status.in_reply_to_status_id:
        logger.info(
            f"'in_reply_to_status_id' : '{status.in_reply_to_status_id}' returned from Status with ID : '{status.id}'"
        )
        return status.in_reply_to_status_id
    else:
        logger.info(
            f"No 'in_reply_to_status_id' found in Status with ID : '{status.id}'"
        )
        return None


@exception(logger)
def get_video_urls_from_status(status: tweepy.models.Status) -> Union[dict, None]:
    """Get video url (video or  gif) and video thumbnail from tweet

    Args:
        tweet (tweepy.models.Status): a tweet status

    Returns:
        Union[dict, None]: {"video_url":video_url, "thumbnail_url":thumbnail_url}, or None if no media in tweet
    """
    if not hasattr(status, "extended_entities"):
        logger.info(f"No 'extended_entities' in Status with ID : '{status.id}'")
        return None
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
            logger.info(f"Video found in Status with ID : '{status.id}'")
            return {
                "video_url": bitrate_url[max(bitrate_url.keys())],
                "thumbnail_url": thumbnail_url,
            }
    logger.info(f"No video found in Status with ID : '{status.id}'")
    return None


@exception(logger)
def extract_infos_from_status(status: tweepy.models.Status) -> dict:
    """Extract informations from tweet status

    Args:
        tweet (tweepy.models.Status): a tweet status

    Returns:
        dict: informations about the tweet status
    """
    tweet_info = {}
    tweet_info["tweet_id"] = str(status.id)
    tweet_info["user_id"] = str(status.user.id)
    tweet_info["screen_name"] = status.user.screen_name.lower()
    tweet_info["screen_name_at"] = f"@{status.user.screen_name.lower()}"
    if hasattr(status, "full_text"):
        text = status.full_text
    else:
        text = status.text
    tweet_info["text"] = basic_tools.clean_text(text)
    logger.debug(f"Infos from Status with ID : '{tweet_info['tweet_id']}' extracted")
    return tweet_info


@exception(logger)
def is_possibly_sensitive(status: tweepy.models.Status) -> bool:
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
@retry(Exception, tries=3, delay=5, logger=logger)
def post_reply_status(
    settings: config.Settings, text: str, tweet_id: Union[str, int]
) -> str:
    """Post tweet with url to the download page (in reply to tweet_id)

    Args:
        text (str): text with url to the download page
        tweet_id (Union[str, int]): tweet id to reply

    Returns:
        str: Reply Tweet ID
    """
    twitter_api = get_twitter_api(settings=settings)
    status = twitter_api.update_status(status=text, in_reply_to_status_id=tweet_id)
    status_id = str(status.id)
    logger.info(f"Reply sent, reply Status ID : '{status_id}'")
    return status_id


@exception(logger)
def handle_new_status(settings: config.Settings, status: tweepy.models.Status) -> bool:
    """Handle new status received

    Args:
        settings (config.Settings): bot settings
        status (tweepy.models.Status): a tweet Status

    Returns:
        bool: True if the a reply is sent, False either
    """
    try:
        # Check if the tweet is a reply to another
        in_reply_to_status_id = get_in_reply_to_status_id(status=status)
        if not in_reply_to_status_id:
            return False

        else:
            # Get the reply tweet and extract the video url from it (if it exits)
            in_reply_status = get_status(
                settings=settings, tweet_id=in_reply_to_status_id
            )
            urls = get_video_urls_from_status(status=in_reply_status)
            if not urls:
                return False

            else:
                # Extract infos from reply status
                tweet_info = extract_infos_from_status(status=status)
                tweet_info_reply = extract_infos_from_status(status=in_reply_status)

                # Check if its sensitive
                if is_possibly_sensitive(status=in_reply_status):
                    logger.info(
                        f"No reply sent to User : '{tweet_info['screen_name']}', Status with ID : '{tweet_info_reply['tweet_id']}' has ensitive content"
                    )
                    return False

                # Check if the user is banned
                if api_tools.is_banned_user(
                    settings=settings, user_id=tweet_info["user_id"]
                ):
                    logger.info(
                        f"No reply sent to User : '{tweet_info['screen_name']}', this User with ID : '{tweet_info['user_id']}' is banned"
                    )
                    return False

                # Get API access token
                api_access_token = api_tools.get_bearer_token(settings=settings)
                if not api_access_token:
                    logger.info(
                        f"No reply sent to User : '{tweet_info['screen_name']}', access token can not be generated"
                    )
                    return False

                # Create video in DB if it doesnt exist
                video = schemas.VideoCreate(
                    creator_screen_name=tweet_info_reply["screen_name"],
                    text=tweet_info_reply["text"],
                    thumbnail_url=urls["thumbnail_url"],
                    tweet_id=tweet_info_reply["tweet_id"],
                    tweet_url=urls["video_url"],
                    creator_user_id=tweet_info_reply["user_id"],
                    video_url=f'https://twitter.com/twitter/statuses/{tweet_info_reply["tweet_id"]}',
                )
                if (
                    api_tools.create_video_if_doesnt_exist(
                        settings=settings, access_token=api_access_token, video=video
                    )
                    is False
                ):
                    logger.info(
                        f"No reply sent to User : '{tweet_info['screen_name']}', the Video with ID : '{tweet_info_reply['tweet_id']}' is not in DB and can not be created"
                    )
                    return False

                # Create user in DB if he doesnt exist
                user = schemas.UserCreate(
                    screen_name=tweet_info["screen_name"], user_id=tweet_info["user_id"]
                )
                if (
                    api_tools.create_user_if_doesnt_exist(
                        settings=settings, access_token=api_access_token, user=user
                    )
                    is False
                ):
                    logger.info(
                        f"No reply sent to User : '{tweet_info['screen_name']}', the User : '{tweet_info['screen_name']}' is not in DB and can not be created"
                    )
                    return False

                # Check if user already asked this video
                if api_tools.get_videouserlink_by_screen_name_and_tweet_id(
                    settings=settings,
                    screen_name=tweet_info["screen_name"],
                    tweet_id=tweet_info_reply["tweet_id"],
                ):
                    logger.info(
                        f"No reply sent to User : '{tweet_info['screen_name']}', Video with ID '{tweet_info_reply['tweet_id']}' already requested by User"
                    )
                    return False

                # Check if video was asked more than settings.ASKED_COUNT_MAX times
                video_count = api_tools.get_video_count_by_tweet_id(
                    settings=settings, tweet_id=tweet_info_reply["tweet_id"]
                )
                if video_count:
                    if video_count >= settings.ASKED_COUNT_MAX:
                        logger.info(
                            f"No reply sent to User : '{tweet_info['screen_name']}', Video with ID '{tweet_info_reply['tweet_id']}' requested to many time : {video_count}"
                        )
                        return False

                # Post status
                text = f'{tweet_info["screen_name_at"]} Download link here! \n{os.path.join(settings.URL_PREFIX, tweet_info_reply["tweet_id"])}'
                reply_status_id = post_reply_status(
                    settings=settings, text=text, tweet_id=str(status.id)
                )

                # Create videouserlink in DB
                videuserlink = schemas.VideoUserLinkCreate(
                    tweet_id=tweet_info_reply["tweet_id"],
                    reply_tweet_id=reply_status_id,
                )
                api_tools.create_videouserlink(
                    settings=settings,
                    access_token=api_access_token,
                    videouserlink=videuserlink,
                    screen_name=tweet_info["screen_name"],
                )

                return True

    except Exception as e:
        logger.error(f"Error occured : {e}")
