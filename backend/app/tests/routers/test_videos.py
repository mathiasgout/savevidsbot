from wsgi import app
from api import dependencies, config
from api.tools import twitter_tools
from tests import overrided_dependencies, sample_db

import pytest
from fastapi.testclient import TestClient


app.dependency_overrides[
    dependencies.get_current_admin
] = overrided_dependencies.override_get_current_admin
app.dependency_overrides[dependencies.get_db] = overrided_dependencies.override_get_db
app.dependency_overrides[
    config.get_settings
] = overrided_dependencies.override_get_settings

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def create_and_remove_sample_db():

    db = next(overrided_dependencies.override_get_db())

    # Création des éléments des tables
    sample_db.create_sample_dataset(db=db)

    yield

    # Suppression des éléments des tables
    sample_db.delete_sample_dataset(db=db)


@pytest.fixture(autouse=True)
def setup_mock(mocker):
    # On mock la fonction "twitter_tools.delete_tweet"
    # pour que la vrai fonction ne soit pas executée avec l'appel routes
    mocker.patch("api.tools.twitter_tools.delete_tweet")


""" Début des tests """
# GET
def test_get_last_ALL_GOOD():
    response = client.get("/api/v2/videos/latest")
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]["tweet_id"] == "111"
    assert response.json()[2]["tweet_id"] == "222"
    assert response.json()[1]["creator_screen_name"] == "creator_screen_name3"


def test_get_last_ALL_GOOD_SKIP():
    response = client.get("/api/v2/videos/latest?skip=1")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[1]["tweet_id"] == "222"
    assert response.json()[0]["creator_screen_name"] == "creator_screen_name3"


def test_get_last_ALL_GOOD_LIMIT():
    response = client.get("/api/v2/videos/latest?limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["tweet_id"] == "111"
    assert response.json()[0]["creator_screen_name"] == "creator_screen_name"


def test_get_last_ALL_GOOD_SKIP_LIMIT():
    response = client.get("/api/v2/videos/latest?skip=1&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["tweet_id"] == "333"
    assert response.json()[1]["tweet_id"] == "222"
    assert response.json()[0]["creator_screen_name"] == "creator_screen_name3"


def test_get_last_ALL_GOOD_SKIP_LIMIT_TOO_FAR():
    response = client.get("/api/v2/videos/latest?skip=2&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["tweet_id"] == "222"
    assert response.json()[0]["creator_screen_name"] == "creator_screen_name2"


def test_get_last_NO_VIDEO_SKIP_LIMIT_TOO_FAR():
    response = client.get("/api/v2/videos/latest?skip=3&limit=2")
    assert response.status_code == 404
    assert response.json() == {"detail": "No video"}


def test_get_video_id_GOOD_VIDEO():
    response = client.get("/api/v2/videos/111")
    assert response.status_code == 200
    assert response.json() == {
        "creator_screen_name": "creator_screen_name",
        "text": "text",
        "thumbnail_url": "https://thumbnail_url.com",
        "tweet_id": "111",
        "tweet_url": "https://tweet_url.com",
        "creator_user_id": "111",
        "video_url": "https://video_url.com",
        "id": 1,
        "is_deleted": False,
    }


def test_get_video_id_WRONG_VIDEO():
    response = client.get("/api/v2/videos/000")
    assert response.status_code == 404
    assert response.json() == {"detail": "Video not found"}


def test_get_video_id_videos_link_GOOD_VIDEO():
    response = client.get("/api/v2/videos/111/users_link")
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]["tweet_id"] == "111"
    assert response.json()[1]["screen_name"] == "joseph"


def test_get_video_id_videos_link_GOOD_VIDEO_SKIP():
    response = client.get("/api/v2/videos/111/users_link?skip=1")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["screen_name"] == "joseph"


def test_get_video_id_videos_link_GOOD_VIDEO_LIMIT():
    response = client.get("/api/v2/videos/111/users_link?limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["screen_name"] == "charles"


def test_get_video_id_videos_link_GOOD_VIDEO_SKIP_LIMIT():
    response = client.get("/api/v2/videos/111/users_link?skip=1&limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["screen_name"] == "joseph"


def test_get_video_id_videos_link_WRONG_VIDEO():
    response = client.get("/api/v2/videos/000/users_link")
    assert response.status_code == 404
    assert response.json() == {"detail": "Video not requested"}


def test_get_video_id_video_count_GOOD_VIDEO():
    response = client.get("/api/v2/videos/333/videos_count")
    assert response.status_code == 200
    assert response.json() == {"tweet_id": "333", "videos_count": 1}


def test_get_video_id_video_count_WRONG_VIDEO():
    response = client.get("/api/v2/videos/000/videos_count")
    assert response.status_code == 404
    assert response.json() == {"detail": "This video was not requested"}


# POST
def test_post_GOOD_VIDEO():
    response = client.post(
        "/api/v2/videos",
        json={
            "creator_screen_name": "creator_screen_name9",
            "text": "text9",
            "thumbnail_url": "https://thumbnail_url.com9",
            "tweet_id": "999",
            "tweet_url": "https://tweet_url.com9",
            "creator_user_id": "999",
            "video_url": "https://video_url.com9",
        },
        headers={"Authorization": "Bearer good-token"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "creator_screen_name": "creator_screen_name9",
        "text": "text9",
        "thumbnail_url": "https://thumbnail_url.com9",
        "tweet_id": "999",
        "tweet_url": "https://tweet_url.com9",
        "creator_user_id": "999",
        "video_url": "https://video_url.com9",
        "id": 5,
        "is_deleted": False,
    }


def test_post_ALREADY_REGISTRED_VIDEO():
    response = client.post(
        "/api/v2/videos",
        json={
            "creator_screen_name": "creator_screen_name",
            "text": "text",
            "thumbnail_url": "https://thumbnail_url.com",
            "tweet_id": "111",
            "tweet_url": "https://tweet_url.com",
            "creator_user_id": "111",
            "video_url": "https://video_url.com",
        },
        headers={"Authorization": "Bearer good-token"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Video with tweet_id : 111 already registred"}


# DELETE
def test_delete_video_id_GOOD_VIDEOS_TWEET_FALSE():
    response = client.delete(
        "/api/v2/videos/111?tweet=false",
        headers={"Authorization": "Bearer good-token"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "tweet_id": "111",
        "videouserlink_deleted_count": 3,
    }


def test_delete_video_id_GOOD_VIDEOS_TWEET_TRUE():
    response = client.delete(
        "/api/v2/videos/222?tweet=true",
        headers={"Authorization": "Bearer good-token"},
    )
    settings = overrided_dependencies.override_get_settings()

    # Check pour voir si "twitter_tools.delete_tweet" a été executé (la fonction est mocké)
    twitter_tools.delete_tweet.assert_called_once_with(
        settings=settings, tweet_id="0002"
    )

    assert response.status_code == 200
    assert response.json() == {
        "tweet_id": "222",
        "videouserlink_deleted_count": 1,
    }


def test_delete_video_id_WRONG_USER():
    response = client.delete(
        "/api/v2/videos/000?tweet=false",
        headers={"Authorization": "Bearer good-token"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Video not found"}


def test_delete_video_id_NO_AUTH():
    response = client.delete("/api/v2/videos/333?tweet=false")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}
