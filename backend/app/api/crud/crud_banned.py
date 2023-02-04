from api import logger, models, schemas
from api.tools import basic_tools
from api.tools.error_tools import exception, retry

from sqlalchemy.orm import Session


# Write to database
@exception(logger)
@retry(Exception, tries=3, delay=3, logger=logger)
def create_banned(db: Session, banned: schemas.BannedCreate) -> models.Banned:
    """Create banned

    Args:
        db (Session): DB session
        banned (schemas.BannedCreate): schemas.BannedCreate instance

    Returns:
        models.Banned: models.Banned instance
    """
    db_banned = models.Banned(**banned.dict())
    db.add(db_banned)
    db.commit()
    db.refresh(db_banned)
    logger.info(f"Banned : {db_banned} created")
    return db_banned


@exception(logger)
@retry(Exception, tries=3, delay=3, logger=logger)
def update_banned(db: Session, db_banned: models.Banned, reason: str) -> models.Banned:
    """Edit "reason" and "bannet_at" fields of a banned

    Args:
        db (Session): DB session
        db_banned (models.Banned): models.Banned instance (before edition)
        reason (str): banned reason

    Returns:
        models.Banned: models.Banned instance (after edition)
    """
    db_banned.banned_at = basic_tools.get_timestamp_utc()
    db_banned.reason = reason
    db.commit()
    db.refresh(db_banned)
    logger.info(f"Banned : {db_banned} edited")
    return db_banned


# Read from database
@exception(logger)
def get_banned_by_used_id(db: Session, user_id: str) -> models.Banned:
    """Get a benned by user_id

    Args:
        db (Session): DB session
        user_id (str): banned user_id

    Returns:
        models.Banned: models.Banned instance
    """
    return db.query(models.Banned).filter(models.Banned.user_id == user_id).first()


# Delete from database
@exception(logger)
@retry(Exception, tries=3, delay=3, logger=logger)
def delete_banned(db: Session, db_banned: models.Banned) -> models.Banned:
    """Delete a banned

    Args:
        db (Session): DB session
        db_banned (models.Banned): models.Banned to delete instance

    Returns:
        models.Banned: models.Banned deteted instance
    """
    db.delete(db_banned)
    db.commit()
    logger.info(f"Banned : {db_banned} deleted")
    return db_banned
