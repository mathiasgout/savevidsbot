from api.tools.error_tools import get_logger

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DatabaseError, IntegrityError


logger = get_logger(logger_name=__name__)


def create_app():
    """
    Create and configure the app
    """

    app = FastAPI()

    # Handling Errors
    @app.exception_handler(500)
    async def internal_server_error_exception_handler(request: Request, exc: Exception):
        return JSONResponse(status_code=500, content={"detail": str(exc)})

    from .routers import users, videos, auth, banned
    from .internal import admin

    app.include_router(users.router)
    app.include_router(videos.router)
    app.include_router(banned.router)
    app.include_router(auth.router)
    app.include_router(admin.router)

    return app
