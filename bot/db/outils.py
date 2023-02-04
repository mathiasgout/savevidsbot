from db import logger
from helpers.logger import exception

from typing import List, Dict


@exception(logger)
def get_new_requested_videos(
    video_id: str, requested_videos: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    """Get new requested videos without duplicate
    Args:
        video_id (str): the video id which must not be duplicated
        requested_videos (List[Dict[str, str]]): requested videos from user
    Returns:
        List[Dict[str, str]]: the new requested videos list without duplicate
    """
    new_requested_videos = []
    for d in requested_videos:
        if d["video_id"] != video_id:
            new_requested_videos.append(d)

    return new_requested_videos
