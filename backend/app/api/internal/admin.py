from api import schemas, dependencies

from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/api/v2", tags=["admin"], responses={404: {"description": "Not found"}}
)


@router.get("/admin", response_model=schemas.Admin)
async def admin(current_admin: schemas.Admin = Depends(dependencies.get_current_admin)):
    """Get authenticate admin

    Args:
        current_admin (schemas.Admin, optional): authenticate admin. Defaults to Depends(dependencies.get_current_admin).

    Returns:
        schemas.Admin: authenticate admin
    """
    return current_admin
