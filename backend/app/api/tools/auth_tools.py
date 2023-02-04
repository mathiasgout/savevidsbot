from api import logger, schemas
from api.crud import crud_admins
from api.tools.error_tools import exception

from datetime import datetime, timedelta
from typing import Union

from sqlalchemy.orm import Session
from jose import jwt


@exception(logger)
def verify_password(
    pwd_context, plain_password: str, hashed_password: str
) -> Union[bool, Exception]:
    """Checks if a password matches its hashed version

    Args:
        pwd_context (passlib.context.CryptContext): crypto context
        plain_password (str): password
        hashed_password (str): hashed password

    Returns:
        Union[bool, Exception]: True if password verified, Flase if not, Exception if context and hashed password dont match
    """
    return pwd_context.verify(plain_password, hashed_password)


@exception(logger)
def get_password_hash(pwd_context, password: str) -> str:
    """Hash a password

    Args:
        pwd_context (passlib.context.CryptContext): crypto context
        password (str): password

    Returns:
        str: hashed password
    """
    return pwd_context.hash(password)


@exception(logger)
def get_admin(db: Session, username: str) -> Union[schemas.Admin, None]:
    """Returns Admin if he exists

    Args:
        db (Session): sqlalchemy DB Session
        username (str): admin's username

    Returns:
        Union[schemas.Admin, None]: Admin instance of the admin if he exists, or None
    """
    admin = crud_admins.get_admin_by_username(db=db, username=username)
    if admin:
        return schemas.Admin(username=admin.username, id=admin.id)
    return None


@exception(logger)
def get_admin_with_password(
    db: Session, username: str
) -> Union[schemas.AdminCreate, None]:
    """Returns AdminCreate if he exists

    Args:
        db (Session): sqlalchemy DB Session
        username (str): admin's username

    Returns:
        Union[schemas.AdminCreate, None]: AdminCreate instance of the admin if he exists, or None
    """
    admin = crud_admins.get_admin_by_username(db=db, username=username)
    if admin:
        return schemas.AdminCreate(
            username=admin.username, hashed_password=admin.hashed_password
        )
    return None


@exception(logger)
def authenticate_admin(
    db: Session, pwd_context, username: str, password: str
) -> Union[schemas.AdminCreate, None]:
    """Authenticate an admin

    Args:
        db (Session): sqlalchemy DB Session
        pwd_context (passlib.context.CryptContext): crypto context
        username (str): Admin's username
        password (str): Admin's password

    Returns:
        Union[schemas.AdminCreate, None]: AdminCreate instance of the admin if he passwords matches, or False
    """
    admincreate = get_admin_with_password(db=db, username=username)
    if not admincreate:
        return False
    if not verify_password(
        pwd_context=pwd_context,
        plain_password=password,
        hashed_password=admincreate.hashed_password,
    ):
        return False
    logger.info(f"Admin : username='{username}' autenticated")
    return admincreate


@exception(logger)
def create_access_token(settings, data: dict, expires_delta: Union[int, None] = None):
    """Create an access token

    Args:
        settings (Settings): API settings
        data (dict): Data to link username with the access token
        expires_delta (Union[int, None], optional): access token duration (in minutes). Defaults to None.

    Returns:
        _type_: access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    logger.info("Access token created")
    return encoded_jwt
