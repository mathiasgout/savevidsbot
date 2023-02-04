from api.config import Settings
from tests.conftest import engine

from fastapi import HTTPException, status, Request
from sqlalchemy.orm import sessionmaker


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    except Exception as e:
        db.rollback()
    finally:
        db.close()


def override_get_settings():
    settings = Settings(
        SECRET_KEY="secret_key",
        TWITTER_API_KEY="twitter_api_key",
        TWITTER_API_KEY_SECRET="twitter_api_key_secret",
        TWITTER_ACCESS_TOKEN="twitter_access_token",
        TWITTER_ACCESS_TOKEN_SECRET="twitter_access_token_secret",
    )
    return settings


async def override_get_current_admin(request: Request):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    auth_header = request.headers.get("authorization")
    if auth_header:
        token = auth_header.split()[-1]
        if token == "good-token":
            return {"id": 1, "username": "david"}
    raise credentials_exception
