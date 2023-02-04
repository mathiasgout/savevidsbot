from api import logger, models, schemas
from api.tools.error_tools import exception, retry

from typing import List

from sqlalchemy import desc
from sqlalchemy.orm import Session


# Write to database
@exception(logger)
@retry(Exception, tries=3, delay=3, logger=logger)
def create_video(db: Session, video: schemas.VideoCreate) -> models.Video:
    """Create a video

    Args:
        db (Session): DB session
        video (schemas.VideoCreate): schemas.VideoCreate instance

    Returns:
        models.Video: models.Video instance
    """
    db_video = models.Video(**video.dict())
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    logger.info(f"Video : {db_video} created")
    return db_video


# Read from database
@exception(logger)
def get_videos_of_user_by_screen_name(
    db: Session, screen_name: str, skip: int = 0, limit: int = 100
) -> List[models.Video]:
    """Get a list of videos requested by a user (by user screen_name),
    ordered by requested date desc

    Args:
        db (Session): DB session
        screen_name (str): user screen_name
        skip (int, optional): Number of videos to skip. Defaults to 0.
        limit (int, optional): Number of video to get. Defaults to 100.

    Returns:
        List[models.Video]: A list of models.Video instance
    """
    return (
        db.query(models.Video)
        .join(models.VideoUserLink)
        .filter(models.VideoUserLink.screen_name == screen_name)
        .order_by(desc(models.VideoUserLink.asked_at))
        .limit(limit)
        .offset(skip)
        .all()
    )


@exception(logger)
def get_video_by_tweet_id(db: Session, tweet_id: str) -> models.Video:
    """Get a video by tweet_id

    Args:
        db (Session): DB session
        tweet_id (str): video tweet_id

    Returns:
        models.Video: models.Video instance
    """
    return db.query(models.Video).filter(models.Video.tweet_id == tweet_id).first()


# Delete from database
@exception(logger)
@retry(Exception, tries=3, delay=3, logger=logger)
def delete_video(db: Session, db_video: models.Video) -> models.Video:
    """Delete a video

    Args:
        db (Session): DB session
        db_video (models.Video): models.Video to delete instance

    Returns:
        models.Video: models.Video deleted instance
    """
    db.delete(db_video)
    db.commit()
    logger.info(f"Video : {db_video} deleted")
    return db_video
