from twitter_bot import logger, config, schemas
from twitter_bot.tools.error_tools import exception, retry

import os
from typing import Union

import requests


@exception(logger)
@retry(Exception, tries=3, delay=3, logger=logger)
def is_banned_user(settings: config.Settings, user_id: str) -> bool:
    """Check if a user is banned

    Args:
        settings (config.Settings): bot settings
        user_id (str): User user_id

    Returns:
        bool: True if the User is banned, False either
    """
    r_get_banned = requests.get(os.path.join(settings.API_PREFIX, "banned", user_id))
    if r_get_banned.status_code == 200:
        return True
    return False


@exception(logger)
@retry(Exception, tries=3, delay=3, logger=logger)
def create_video_if_doesnt_exist(
    settings: config.Settings, video: schemas.VideoCreate
) -> bool:
    """Create a Video if it doesn't exist

    Args:
        settings (config.Settings): bot settings
        video (schemas.VideoCreate): schemas.VideoCreate instance

    Returns:
        bool: True if the Video is created or already exists, False either
    """
    r_get_video = requests.get(
        os.path.join(settings.API_PREFIX, "videos", video.tweet_id)
    )
    if r_get_video.status_code == 200:
        return True

    r_post_video = requests.post(
        os.path.join(settings.API_PREFIX, "videos"), json=video.dict()
    )
    if r_post_video.status_code == 200:
        return True
    return False


@exception(logger)
@retry(Exception, tries=3, delay=3, logger=logger)
def create_user_if_doesnt_exist(
    settings: config.Settings, user: schemas.UserCreate
) -> bool:
    """Create a User if he doesn't exist

    Args:
        settings (config.Settings): bot settings
        user (schemas.UserCreate): schemas.UserCreate instance

    Returns:
        bool: True if the Video is created or already exists, False either
    """
    r_get_user = requests.get(
        os.path.join(settings.API_PREFIX, "users", user.screen_name)
    )
    if r_get_user.status_code == 200:
        return True

    r_post_user = requests.post(
        os.path.join(settings.API_PREFIX, "users"), json=user.dict()
    )
    if r_post_user.status_code == 200:
        return True
    return False


@exception(logger)
@retry(Exception, tries=3, delay=3, logger=logger)
def create_videouserlink(
    settings: config.Settings,
    videouserlink: schemas.VideoUserLinkCreate,
    screen_name: str,
) -> bool:
    """Create a link between a User and Video

    Args:
        settings (config.Settings): bot settings
        videouserlink (schemas.VideoUserLinkCreate): schemas.VideoUserLinkCreate instance
        screen_name (str): User screen_name

    Returns:
        bool: True if the VideoUserLink is created or already exists, False either
    """
    r_post_videouserlink = requests.post(
        os.path.join(settings.API_PREFIX, "users", screen_name, "videos_link"),
        json=videouserlink.dict(),
    )
    if r_post_videouserlink.status_code == 200:
        return True
    return False


@exception(logger)
@retry(Exception, tries=3, delay=3, logger=logger)
def get_videouserlink_by_screen_name_and_tweet_id(
    settings: config.Settings, screen_name: str, tweet_id: str
) -> bool:
    """Get a link between a User and a Video

    Args:
        settings (config.Settings): bot settings
        screen_name (str): User screen_name
        tweet_id (str): Video tweet_id

    Returns:
        bool: True if the link exists, False either
    """
    r_get_videouserlink = requests.get(
        os.path.join(settings.API_PREFIX, "users", screen_name, "videos_link", tweet_id)
    )
    if r_get_videouserlink.status_code == 200:
        return True
    return False


@exception(logger)
@retry(Exception, tries=1, delay=3, logger=logger)
def get_video_count_by_tweet_id(
    settings: config.Settings, tweet_id: str
) -> Union[int, None]:
    """Get the number of time a Video is requested

    Args:
        settings (config.Settings): bot settings
        tweet_id (str): Video tweet_id

    Returns:
        Union[int, None]: The number of times a Video is requested, or None if the Video was not requested
    """
    r_videos_count = requests.get(
        os.path.join(settings.API_PREFIX, "videos", tweet_id, "videos_count")
    )
    if r_videos_count.status_code == 200:
        return r_videos_count.json()["videos_count"]
    return None
