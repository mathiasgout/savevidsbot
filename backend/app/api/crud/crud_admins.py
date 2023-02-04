from api import logger, models, schemas
from api.tools.error_tools import exception, retry

from sqlalchemy.orm import Session


# Write to database
@exception(logger)
@retry(Exception, tries=3, delay=3, logger=logger)
def create_admin(db: Session, admin: schemas.AdminCreate) -> models.Admin:
    """Create an admin

    Args:
        db (Session): DB session
        admin (schemas.AdminCreate): schemas.AdminCreate instane

    Returns:
        models.Admin: models.Admin instance
    """
    db_admin = models.Admin(**admin.dict())
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    logger.info(f"Admin : {db_admin} created")
    return db_admin


# Read from database
@exception(logger)
def get_admin_by_username(db: Session, username: str) -> models.Admin:
    """Get an admin by username

    Args:
        db (Session): DB session
        username (str): admin usernmae

    Returns:
        models.Admin: models.Admin instance
    """
    return db.query(models.Admin).filter(models.Admin.username == username).first()
