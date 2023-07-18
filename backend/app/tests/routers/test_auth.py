from wsgi import app
from api import dependencies, config, schemas
from api.crud import crud_admins, crud_misc
from tests import overrided_dependencies

import pytest
from fastapi.testclient import TestClient


app.dependency_overrides[dependencies.get_db] = overrided_dependencies.override_get_db
app.dependency_overrides[
    config.get_settings
] = overrided_dependencies.override_get_settings

client = TestClient(app)


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
    )

    yield

    # Suppression des éléments des tables
    crud_misc.delete_all_rows_of_table(db=db, table_name="Admin")


""" Début des tests """


def test_login_GOOD_AUTH():
    response = client.post(
        "/api/v2/auth/login",
        data={
            "username": "admin",
            "password": "password",
        },
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert "access_token" in response.json().keys()


def test_login_WRONG_AUTH():
    response = client.post(
        "/api/v2/auth/login",
        data={
            "username": "admin",
            "password": "password2",
        },
    )
    assert response.status_code == 401


def test_login_NO_AUTH():
    response = client.post("/api/v2/auth/login")
    assert response.status_code == 422
