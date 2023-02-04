from api import schemas, dependencies
from api.crud import crud_banned, crud_users

from fastapi import APIRouter, Path, Depends, HTTPException
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/api/v2/banned",
    tags=["banned"],
    responses={404: {"description": "Not found"}},
)


# GET
@router.get("/{user_id}", response_model=schemas.Banned)
async def read_banned(
    user_id: str = Path(min_length=3, regex="^[0-9]*$"),
    db: Session = Depends(dependencies.get_db),
):
    """Get a banned user

    Args:
        user_id (str): banned user_id. Defaults to Path(min_length=5).
        db (Session, optional): DB Session. Defaults to Depends(dependencies.get_db).

    Raises:
        HTTPException: HTTP 404

    Returns:
        schemas.User: schemas.Banned instance
    """
    db_banned = crud_banned.get_banned_by_used_id(db, user_id=user_id)
    if db_banned is None:
        raise HTTPException(status_code=404, detail="Banned not found")
    return db_banned


# POST
@router.post("", response_model=schemas.Banned)
async def create_banned(
    banned: schemas.BannedCreate,
    db: Session = Depends(dependencies.get_db),
):
    """Create a banned user
    Args:
        banned (schemas.BannedCreate): schemas.BannedCreate instance
        db (Session, optional): DB session. Defaults to Depends(dependencies.get_db).

    Raises:
        HTTPException: HTTP 404

    Returns:
        schemas.Banned: schemas.Banned instance
    """
    # Get the user
    db_users = crud_users.get_users_by_user_id(db, user_id=banned.user_id, limit=1)
    if not db_users:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if banned exists
    db_banned = crud_banned.get_banned_by_used_id(db=db, user_id=banned.user_id)
    if db_banned:
        return crud_banned.update_banned(
            db=db, db_banned=db_banned, reason=banned.reason
        )

    return crud_banned.create_banned(db=db, banned=banned)
