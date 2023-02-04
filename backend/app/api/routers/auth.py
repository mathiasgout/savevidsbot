from api import schemas, config, dependencies
from api.tools import auth_tools

from fastapi import APIRouter, Depends, HTTPException, status, security
from passlib.context import CryptContext
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v2/auth", tags=["login"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(
    form_data: security.OAuth2PasswordRequestForm = Depends(),
    settings: config.Settings = Depends(config.get_settings),
    db: Session = Depends(dependencies.get_db),
):
    """Generate access token for an authenticate admin

    Args:
        form_data (security.OAuth2PasswordRequestForm, optional): A from with authenticate informations. Defaults to Depends().
        settings (config.Settings, optional): API settings. Defaults to Depends(config.get_settings).
        db (Session, optional): DB session. Defaults to Depends(dependencies.get_db).

    Raises:
        HTTPException: HTTP 401 UNAUTHORIZED

    Returns:
        schemas.Token: Access token
    """

    # try to authenticate with data in the post request
    admin = auth_tools.authenticate_admin(
        db=db,
        pwd_context=pwd_context,
        username=form_data.username,
        password=form_data.password,
    )
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # if autenticated, create an access token and returns it
    access_token_expires = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    access_token = auth_tools.create_access_token(
        settings=settings,
        data={"sub": admin.username},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
