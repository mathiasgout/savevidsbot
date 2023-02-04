from api import config, schemas, database
from api.tools import auth_tools

from fastapi import Depends, HTTPException, status, security
from sqlalchemy.orm import Session
from jose import JWTError, jwt

# Check si la requête à un header "Authorization" avec "Bearer + un token" et renvoie le token
# Si il n'y a pas de header "Authorization" ou de token "Bearer", renvoie une erreur HTTP 401
# "tokenUrl" est l'URL que le client peut utiliser pour envoyer un "username" et un "password" dans le but d'avoir un token
oauth2_scheme = security.OAuth2PasswordBearer(tokenUrl="/api/v2/auth/login")


def get_db() -> Session:
    """Generate a DB session

    Yields:
        Session: DB session
    """
    db = database.SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
    finally:
        db.close()


async def get_current_admin(
    token: str = Depends(oauth2_scheme),
    settings: config.Settings = Depends(config.get_settings),
    db: Session = Depends(get_db),
) -> schemas.Admin:
    """Returns the admin who is logged in

    Args:
        token (str, optional): An access token. Defaults to Depends(oauth2_scheme).
        settings (Settings, optional): The API settings. Defaults to Depends(get_settings).
        db (Session, optional): sqlalchemy DB Session. Defaults to Depends(get_db).

    Raises:
        credentials_exception: HTTP 401 UNAUTHORIZED

    Returns:
        AdminCreate: AdminCreate instance
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # try to decode the access token and extract the username
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    # if the access token is not fake and the admin exists, returns and Admin instance
    admin = auth_tools.get_admin(db=db, username=token_data.username)
    if admin is None:
        raise credentials_exception
    return admin
