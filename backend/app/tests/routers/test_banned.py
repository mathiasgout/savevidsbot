from wsgi import app
from api import dependencies, schemas
from api.crud import crud_users, crud_banned, crud_misc
from tests import overrided_dependencies

import pytest
from fastapi.testclient import TestClient


app.dependency_overrides[dependencies.get_db] = overrided_dependencies.override_get_db
app.dependency_overrides[
    dependencies.get_current_admin
] = overrided_dependencies.override_get_current_admin

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def create_and_remove_sample_db():

    db = next(overrided_dependencies.override_get_db())

    # Création des éléments des tables
    crud_users.create_user(
        db=db, user=schemas.UserCreate(screen_name="david", user_id="111")
    )  # id=1
    crud_users.create_user(
        db=db, user=schemas.UserCreate(screen_name="joseph", user_id="222")
    )  # id=2
    crud_users.create_user(
        db=db, user=schemas.UserCreate(screen_name="marcel", user_id="111")
    )  # id=3
    crud_users.create_user(
        db=db, user=schemas.UserCreate(screen_name="gauthier", user_id="333")
    )  # id=3

    crud_banned.create_banned(
        db=db, banned=schemas.BannedCreate(user_id="111", reason="SEX")
    )

    yield

    # Suppression des éléments des tables
    crud_misc.delete_all_rows_of_table(db=db, table_name="User")
    crud_misc.delete_all_rows_of_table(db=db, table_name="Banned")


""" Début des tests """
# GET
def test_get_user_id_GOOD_USER():
    response = client.get("/api/v2/banned/111")
    assert response.status_code == 200
    assert response.json()["user_id"] == "111"
    assert response.json()["reason"] == "SEX"


def test_get_user_id_WRONG_USER():
    response = client.get("/api/v2/banned/555")
    assert response.status_code == 404
    assert response.json() == {"detail": "Banned not found"}


# POST
def test_post_user_id_ban_GOOD_USER():
    response = client.post(
        "/api/v2/banned",
        json={"user_id": "222", "reason": "DRUG"},
        headers={"Authorization": "Bearer good-token"},
    )
    assert response.status_code == 200
    assert response.json()["user_id"] == "222"
    assert response.json()["reason"] == "DRUG"


def test_post_user_id_ban_GOOD_USER_REBAN():
    response = client.post(
        "/api/v2/banned",
        json={"user_id": "111", "reason": "DRUG"},
        headers={"Authorization": "Bearer good-token"},
    )
    assert response.status_code == 200
    assert response.json()["user_id"] == "111"
    assert response.json()["reason"] == "DRUG"


def test_post_user_id_ban_WRONG_USER():
    response = client.post(
        "/api/v2/banned",
        json={"user_id": "555", "reason": "DRUG"},
        headers={"Authorization": "Bearer good-token"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
