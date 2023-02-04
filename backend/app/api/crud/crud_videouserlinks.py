from api import logger, models, schemas
from api.tools.error_tools import exception, retry

from typing import List

from sqlalchemy import desc
from sqlalchemy.orm import Session


# Write to database
@exception(logger)
@retry(Exception, tries=3, delay=3, logger=logger)
def create_videouserlink(
    db: Session, videouserlink: schemas.VideoUserLinkCreate, screen_name: str
) -> models.VideoUserLink:
    """Create a videouserlink

    Args:
        db (Session): DB session
        videouserlink (schemas.VideoUserLinkCreate): schemas.VideoUserLinkCreate instance
        screen_name (str): user screen_name

    Returns:
        models.VideoUserLink: models.VideoUserLink instance
    """
    db_videouserlink = models.VideoUserLink(
        **videouserlink.dict(), screen_name=screen_name
    )
    db.add(db_videouserlink)
    db.commit()
    db.refresh(db_videouserlink)
    logger.info(f"VideoUserLink : {db_videouserlink} created")
    return db_videouserlink


# Read from database
@exception(logger)
def get_videouserlink_by_screen_name_and_tweet_id(
    db: Session, screen_name: str, tweet_id: str
) -> models.VideoUserLink:
    """Get a videouserlink by user screen_name and video tweet_id

    Args:
        db (Session): DB session
        screen_name (str): user screen_name
        tweet_id (str): video tweet_id

    Returns:
        models.VideoUserLink: models.VideoUserLink instance
    """
    return (
        db.query(models.VideoUserLink)
        .filter(models.VideoUserLink.screen_name == screen_name)
        .filter(models.VideoUserLink.tweet_id == tweet_id)
        .first()
    )


@exception(logger)
def get_videouserlink_by_reply_tweet_id(
    db: Session, reply_tweet_id: str
) -> models.VideoUserLink:
    """Get a videouserlink by reply_tweet_id

    Args:
        db (Session): DB session
        reply_tweet_id (str): videouserlink reply_tweet_id

    Returns:
        models.VideoUserLink: models.VideoUserLink instance
    """
    return (
        db.query(models.VideoUserLink)
        .filter(models.VideoUserLink.reply_tweet_id == reply_tweet_id)
        .first()
    )


@exception(logger)
def get_videouserlinks_by_tweet_id(
    db: Session, tweet_id: str, skip: int = 0, limit: int = 100
) -> List[models.VideoUserLink]:
    """Get a list of videouserlink by video tweet_id,
    ordered by requested date desc

    Args:
        db (Session): DB session
        tweet_id (str): video tweet_id
        skip (int, optional): Number of videos to skip. Defaults to 0.
        limit (int, optional): Number of video to get. Defaults to 100.

    Returns:
        List[models.VideoUserLink]: A list of models.VideoUserLink instance
    """
    return (
        db.query(models.VideoUserLink)
        .filter(models.VideoUserLink.tweet_id == tweet_id)
        .order_by(desc(models.VideoUserLink.asked_at))
        .limit(limit)
        .offset(skip)
        .all()
    )


@exception(logger)
def get_videouserlinks_by_screen_name(
    db: Session, screen_name: str, skip: int = 0, limit: int = 100
) -> List[models.VideoUserLink]:
    """Get a list of videouserlink by user screen_name,
    ordered by requested date desc

    Args:
        db (Session): DB session
        screen_name (str): user screen_name
        skip (int, optional): Number of videos to skip. Defaults to 0.
        limit (int, optional): Number of video to get. Defaults to 100.

    Returns:
        List[models.VideoUserLink]: A list of models.VideoUserLink instance
    """
    return (
        db.query(models.VideoUserLink)
        .filter(models.VideoUserLink.screen_name == screen_name)
        .order_by(desc(models.VideoUserLink.asked_at))
        .limit(limit)
        .offset(skip)
        .all()
    )


@exception(logger)
def get_videouserlinks_count_by_screen_name(db: Session, screen_name: str) -> int:
    """Get the number of videouserlinks by user screen_name

    Args:
        db (Session): DB session
        screen_name (str): user screen_name

    Returns:
        int: the number of videouserlinks
    """
    return (
        db.query(models.VideoUserLink)
        .filter(models.VideoUserLink.screen_name == screen_name)
        .count()
    )


@exception(logger)
def get_videouserlinks_count_by_tweet_id(db: Session, tweet_id: str) -> int:
    """Get the number of videouserlinks by video tweet_id

    Args:
        db (Session): DB session
        screen_name (str): video tweet_id

    Returns:
        int: the number of videouserlinks
    """
    return (
        db.query(models.VideoUserLink)
        .filter(models.VideoUserLink.tweet_id == tweet_id)
        .count()
    )


# Delete from database
@exception(logger)
@retry(Exception, tries=3, delay=3, logger=logger)
def delete_videouserlink(
    db: Session, db_videouserlink: models.VideoUserLink
) -> models.VideoUserLink:
    """Delete a videouserlink

    Args:
        db (Session): DB session
        db_videouserlink (models.VideoUserLink): models.VideoUserLink to delete instance

    Returns:
        models.VideoUserLink: models.VideoUserLink deleted instance
    """
    db.delete(db_videouserlink)
    db.commit()
    logger.info(f"VideoUserLink : {db_videouserlink} deleted")
    return db_videouserlink


@exception(logger)
@retry(Exception, tries=3, delay=3, logger=logger)
def delete_videouserlinks_by_screen_name(
    db: Session, screen_name: str
) -> schemas.UserDeleted:
    """Delete a list of videouserlink by user screen_name

    Args:
        db (Session): DB session
        screen_name (str): user screen_name

    Returns:
        schemas.UserDeleted: schemas.UserDeleted instance
    """
    query = db.query(models.VideoUserLink).filter(
        models.VideoUserLink.screen_name == screen_name
    )
    videouserlink_deleted_count = query.count()
    query.delete()
    db.commit()
    logger.info(
        f"VideoUserLinks with screen_name='{screen_name}' deleted ({videouserlink_deleted_count} deletions)"
    )
    return schemas.UserDeleted(
        screen_name=screen_name, videouserlink_deleted_count=videouserlink_deleted_count
    )


@exception(logger)
@retry(Exception, tries=3, delay=3, logger=logger)
def delete_videouserlinks_by_tweet_id(
    db: Session, tweet_id: str
) -> schemas.VideoDeleted:
    """Delete a list of videouserlink by video tweet_id

    Args:
        db (Session): DB session
        tweet_id (str): video tweet_id

    Returns:
        schemas.VideoDeleted: schemas.VideoDeleted instance
    """
    query = db.query(models.VideoUserLink).filter(
        models.VideoUserLink.tweet_id == tweet_id
    )
    videouserlink_deleted_count = query.count()
    query.delete()
    db.commit()
    logger.info(
        f"VideoUserLinks with tweet_id='{tweet_id}' deleted ({videouserlink_deleted_count} deletions)"
    )
    return schemas.VideoDeleted(
        tweet_id=tweet_id, videouserlink_deleted_count=videouserlink_deleted_count
    )
