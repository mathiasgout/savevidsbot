from api import schemas
from api.crud import crud_admins, crud_misc
from api.tools import auth_tools
from tests import overrided_dependencies

import pytest
from passlib.context import CryptContext


@pytest.fixture(scope="module", autouse=True)
def create_and_remove_sample_db():

    db = next(overrided_dependencies.override_get_db())

    # Création des éléments des tables
    crud_admins.create_admin(
        db=db,
        admin=schemas.AdminCreate(
            username="admin",
            hashed_password="$2b$12$pFxmSTAATdksSbfa5l3q8OlCJol1EAz/WM4agxjmDIaC3o5y98A2G",
        ),
    )  # id=1

    yield

    # Suppression des éléments des tables
    crud_misc.delete_all_rows_of_table(db=db, table_name="Admin")


""" Début des tests """


def test_verify_password_GOOD_PASSWORD():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    assert (
        auth_tools.verify_password(
            pwd_context=pwd_context,
            plain_password="password",
            hashed_password="$2b$12$pFxmSTAATdksSbfa5l3q8OlCJol1EAz/WM4agxjmDIaC3o5y98A2G",
        )
        is True
    )


def test_verify_password_WRONG_PASSWORD():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    assert (
        auth_tools.verify_password(
            pwd_context=pwd_context,
            plain_password="password",
            hashed_password="$2b$12$pFxmSTAATdksSbfa5l3q8OlCJol1EAz/WM4agxjmDPaC3o5y98A2G",
        )
        is False
    )


def test_get_admin_GOOD_ADMIN():
    db = next(overrided_dependencies.override_get_db())
    assert isinstance(auth_tools.get_admin(db=db, username="admin"), schemas.Admin)


def test_get_admin_WRONG_ADMIN():
    db = next(overrided_dependencies.override_get_db())
    assert auth_tools.get_admin(db=db, username="admin2") is None


def test_get_admin_with_password_GOOD_ADMIN():
    db = next(overrided_dependencies.override_get_db())
    assert isinstance(
        auth_tools.get_admin_with_password(db=db, username="admin"), schemas.AdminCreate
    )


def test_get_admin_with_password_WRONG_ADMIN():
    db = next(overrided_dependencies.override_get_db())
    assert auth_tools.get_admin_with_password(db=db, username="admin2") is None


def test_authenticate_admin_GOOD_ADMIN():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    db = next(overrided_dependencies.override_get_db())
    assert isinstance(
        auth_tools.authenticate_admin(
            db=db, pwd_context=pwd_context, username="admin", password="password"
        ),
        schemas.AdminCreate,
    )


def test_authenticate_admin_WRONG_PASSWORD():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    db = next(overrided_dependencies.override_get_db())
    assert (
        auth_tools.authenticate_admin(
            db=db, pwd_context=pwd_context, username="admin", password="password2"
        )
        is False
    )


def test_authenticate_admin_WRONG_ADMIN():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    db = next(overrided_dependencies.override_get_db())
    assert (
        auth_tools.authenticate_admin(
            db=db, pwd_context=pwd_context, username="admin2", password="password"
        )
        is False
    )


def test_create_access_token_NO_EXPIRES_DELTA():
    settings = overrided_dependencies.override_get_settings()
    assert isinstance(
        auth_tools.create_access_token(settings=settings, data={"sub": "admin"}), str
    )


def test_create_access_token_EXPIRES_DELTA():
    settings = overrided_dependencies.override_get_settings()
    assert isinstance(
        auth_tools.create_access_token(
            settings=settings, data={"sub": "admin"}, expires_delta=30
        ),
        str,
    )
