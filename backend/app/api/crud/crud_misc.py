from api import logger, models
from api.tools.error_tools import exception, retry

from sqlalchemy.orm import Session


# Delete from database
@exception(logger)
@retry(Exception, tries=3, delay=3, logger=logger)
def delete_all_rows_of_table(db: Session, table_name: str) -> bool:
    """Delete all row of a table

    Args:
        db (Session): DB session
        table_name (str): table name (model name)

    Returns:
        bool: True if the rows have been deleted
    """
    if table_name == "Video":
        db.query(models.Video).delete()
        db.commit()
        logger.info("All rows from table 'Video' deleted")
        return True
    if table_name == "User":
        db.query(models.User).delete()
        db.commit()
        logger.info("All rows from table 'User' deleted")
        return True
    if table_name == "VideoUserLink":
        db.query(models.VideoUserLink).delete()
        db.commit()
        logger.info("All rows from table 'VideoUserLink' deleted")
        return True
    if table_name == "Banned":
        db.query(models.Banned).delete()
        db.commit()
        logger.info("All rows from table 'Banned' deleted")
        return True
    if table_name == "Admin":
        db.query(models.Admin).delete()
        db.commit()
        logger.info("All rows from table 'Admin' deleted")
        return True
    return False
