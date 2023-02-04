from api import logger, models, schemas
from api.tools.error_tools import exception, retry

from typing import List

from sqlalchemy import desc
from sqlalchemy.orm import Session


# Write to database
@exception(logger)
@retry(Exception, tries=3, delay=3, logger=logger)
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a user

    Args:
        db (Session): DB session
        user (schemas.UserCreate): schemas.UserCreate instance

    Returns:
        models.User: models.User instance
    """
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User : {db_user} created")
    return db_user


# Read from database
@exception(logger)
def get_user_by_screen_name(db: Session, screen_name: str) -> models.User:
    """Get a user by screen_name

    Args:
        db (Session): DB session
        screen_name (str): user screen_name

    Returns:
        models.User: models.User instance
    """
    return db.query(models.User).filter(models.User.screen_name == screen_name).first()


@exception(logger)
def get_users_by_user_id(
    db: Session, user_id: str, skip: int = 0, limit: int = 100
) -> List[models.User]:
    """Get users by user_id

    Args:
        db (Session): DB session
        user_id (str): user user_id
        skip (int, optional): Number of videos to skip. Defaults to 0.
        limit (int, optional): Number of video to get. Defaults to 100.

    Returns:
        List[models.User]: list of models.User instance
    """
    return (
        db.query(models.User)
        .filter(models.User.user_id == user_id)
        .order_by(desc(models.User.screen_name))
        .limit(limit)
        .offset(skip)
        .all()
    )


# Delete from database
@exception(logger)
@retry(Exception, tries=3, delay=3, logger=logger)
def delete_user(db: Session, db_user: models.User) -> models.User:
    """Delete an user

    Args:
        db (Session): DB session
        db_user (models.User): models.User to delete instance

    Returns:
        models.User: models.User deleted instance
    """
    db.delete(db_user)
    db.commit()
    logger.info(f"User : {db_user} deleted")
    return db_user
