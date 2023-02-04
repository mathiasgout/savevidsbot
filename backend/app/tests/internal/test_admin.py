from wsgi import app
from api import dependencies
from tests import overrided_dependencies

from fastapi.testclient import TestClient


client = TestClient(app)


app.dependency_overrides[
    dependencies.get_current_admin
] = overrided_dependencies.override_get_current_admin


def test_admin_GOOD_HEADER():
    response = client.get(
        "/api/v2/admin", headers={"Authorization": "Bearer good-token"}
    )
    assert response.status_code == 200
    assert response.json() == {"id": 1, "username": "david"}


def test_admin_NO_HEADER():
    response = client.get("/api/v2/admin")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_admin_WRONG_HEADER():
    response = client.get(
        "/api/v2/admin", headers={"Authorization": "Bearer wrong-token"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}
