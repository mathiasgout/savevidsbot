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
def test_get_screen_name_GOOD_USER():
    response = client.get("/api/v2/users/david")
    assert response.status_code == 200
    assert response.json() == {"screen_name": "david", "user_id": "1", "id": 1}


def test_get_screen_name_WRONG_USER():
    response = client.get("/api/v2/users/tristan")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_get_screen_name_video_links_video_id_GOOD_USER_GOOD_VIDEO():
    response = client.get("/api/v2/users/david/videos_link/111")
    assert response.status_code == 200
    assert response.json()["tweet_id"] == "111"
    assert response.json()["reply_tweet_id"] == "0001"
    assert response.json()["screen_name"] == "david"


def test_get_screen_name_videos_link_video_id_GOOD_USER_WRONG_VIDEO():
    response = client.get("/api/v2/users/joseph/videos_link/333")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Link between user : 'joseph' and video : '333' not found"
    }


def test_get_screen_name_videos_link_video_id_WRONG_USER_GOOD_VIDEO():
    response = client.get("/api/v2/users/tristan/videos_link/111")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Link between user : 'tristan' and video : '111' not found"
    }


def test_get_screen_name_videos_link_GOOD_USER():
    response = client.get("/api/v2/users/david/videos_link")
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]["tweet_id"] == "333"
    assert response.json()[1]["screen_name"] == "david"


def test_get_screen_name_videos_link_GOOD_USER_SKIP():
    response = client.get("/api/v2/users/david/videos_link?skip=1")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["tweet_id"] == "222"


def test_get_screen_name_videos_link_GOOD_USER_LIMIT():
    response = client.get("/api/v2/users/david/videos_link?limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["tweet_id"] == "333"


def test_get_screen_name_videos_link_GOOD_USER_SKIP_LIMIT():
    response = client.get("/api/v2/users/david/videos_link?skip=1&limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["tweet_id"] == "222"


def test_get_screen_name_videos_link_WRONG_USER():
    response = client.get("/api/v2/users/tristan/videos_link")
    assert response.status_code == 404
    assert response.json() == {"detail": "User does not requested videos"}


def test_get_screen_name_video_count_GOOD_USER():
    response = client.get("/api/v2/users/david/videos_count")
    assert response.status_code == 200
    assert response.json() == {"screen_name": "david", "videos_count": 3}


def test_get_screen_name_video_count_WRONG_USER():
    response = client.get("/api/v2/users/tristan/videos_count")
    assert response.status_code == 404
    assert response.json() == {"detail": "No videos requested by user"}


def test_get_screen_name_videos_GOOD_USER():
    response = client.get("/api/v2/users/david/videos")
    assert response.status_code == 200
    assert response.json()["screen_name"] == "david"
    assert len(response.json()["videos"]) == 3
    assert response.json()["videos"][0]["tweet_id"] == "333"


def test_get_screen_name_videos_WRONG_USER():
    response = client.get("/api/v2/users/tristan/videos")
    assert response.status_code == 404
    assert response.json() == {"detail": "No videos requested by user"}


def test_get_screen_name_videos_GOOD_USER_SKIP():
    response = client.get("/api/v2/users/david/videos?skip=1")
    assert response.status_code == 200
    assert response.json()["screen_name"] == "david"
    assert len(response.json()["videos"]) == 2
    assert response.json()["videos"][0]["tweet_id"] == "222"


def test_get_screen_name_videos_GOOD_USER_LIMIT():
    response = client.get("/api/v2/users/david/videos?limit=1")
    assert response.status_code == 200
    assert response.json()["screen_name"] == "david"
    assert len(response.json()["videos"]) == 1
    assert response.json()["videos"][0]["tweet_id"] == "333"


def test_get_screen_name_videos_GOOD_USER_SKIP_LIMIT():
    response = client.get("/api/v2/users/david/videos?skip=1&limit=1")
    assert response.status_code == 200
    assert response.json()["screen_name"] == "david"
    assert len(response.json()["videos"]) == 1
    assert response.json()["videos"][0]["tweet_id"] == "222"


# POST
def test_post_GOOD_USER():
    response = client.post(
        "/api/v2/users",
        json={"screen_name": "mouloud", "user_id": "100"},
        headers={"Authorization": "Bearer good-token"},
    )
    assert response.status_code == 200
    assert response.json() == {"screen_name": "mouloud", "user_id": "100", "id": 6}


def test_post_ALREADY_REGISTRED_USER():
    response = client.post(
        "/api/v2/users",
        json={"screen_name": "david", "user_id": "3"},
        headers={"Authorization": "Bearer good-token"},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "User with screen_name='david' already registered"
    }


def test_post_screen_name_videos_link_GOOD_USER_GOOD_VIDEO():
    response = client.post(
        "/api/v2/users/olivier/videos_link",
        json={"tweet_id": "111", "reply_tweet_id": "9989"},
        headers={"Authorization": "Bearer good-token"},
    )
    assert response.status_code == 200
    assert response.json()["tweet_id"] == "111"
    assert response.json()["screen_name"] == "olivier"
    assert response.json()["reply_tweet_id"] == "9989"


def test_post_screen_name_videos_link_GOOD_USER_WRONG_VIDEO():
    response = client.post(
        "/api/v2/users/olivier/videos_link",
        json={"tweet_id": "9999", "reply_tweet_id": "23929"},
        headers={"Authorization": "Bearer good-token"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User or video not found"}


def test_post_screen_name_videos_link_WRONG_USER_GOOD_VIDEO():
    response = client.post(
        "/api/v2/users/tristan/videos_link",
        json={"tweet_id": "222", "reply_tweet_id": "48239"},
        headers={"Authorization": "Bearer good-token"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User or video not found"}


def test_post_screen_name_videos_link_ALREADY_REGISTRED():
    response = client.post(
        "/api/v2/users/david/videos_link",
        json={"tweet_id": "111", "reply_tweet_id": "0001"},
        headers={"Authorization": "Bearer good-token"},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Videouserlink already registered with this reply_tweet_id"
    }


# DELETE
def test_delete_screen_name_GOOD_USER_TWEET_FALSE():
    response = client.delete(
        "/api/v2/users/joseph?tweet=false",
        headers={"Authorization": "Bearer good-token"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "screen_name": "joseph",
        "videouserlink_deleted_count": 1,
    }


def test_delete_screen_name_GOOD_USER_TWEET_TRUE():
    response = client.delete(
        "/api/v2/users/charles?tweet=true",
        headers={"Authorization": "Bearer good-token"},
    )
    settings = overrided_dependencies.override_get_settings()

    # Check pour voir si "twitter_tools.delete_tweet" a été executé (la fonction est mocké)
    twitter_tools.delete_tweet.assert_called_once_with(
        settings=settings, tweet_id="0005"
    )

    assert response.status_code == 200
    assert response.json() == {
        "screen_name": "charles",
        "videouserlink_deleted_count": 1,
    }


def test_delete_screen_name_GOOD_USER_W_BANNED():
    response = client.delete(
        "/api/v2/users/gauthier?tweet=false",
        headers={"Authorization": "Bearer good-token"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "screen_name": "gauthier",
        "videouserlink_deleted_count": 0,
    }


def test_delete_screen_name_WRONG_USER():
    response = client.delete(
        "/api/v2/users/tristan?tweet=false",
        headers={"Authorization": "Bearer good-token"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_delete_screen_name_NO_AUTH():
    response = client.delete("/api/v2/users/tristan?tweet=false")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_delete_screen_name_videos_link_video_id_GOOD_USER_GOOD_VIDEO_TWEET_FALSE():
    response = client.delete(
        "/api/v2/users/david/videos_link/111?tweet=false",
        headers={"Authorization": "Bearer good-token"},
    )
    assert response.status_code == 200
    assert response.json()["tweet_id"] == "111"
    assert response.json()["reply_tweet_id"] == "0001"
    assert response.json()["screen_name"] == "david"


def test_delete_screen_name_videos_link_video_id_GOOD_USER_GOOD_VIDEO_TWEET_TRUE():
    response = client.delete(
        "/api/v2/users/david/videos_link/222?tweet=true",
        headers={"Authorization": "Bearer good-token"},
    )
    settings = overrided_dependencies.override_get_settings()

    # Check pour voir si "twitter_tools.delete_tweet" a été executé (la fonction est mocké)
    twitter_tools.delete_tweet.assert_called_once_with(
        settings=settings, tweet_id="0002"
    )
    assert response.status_code == 200
    assert response.json()["tweet_id"] == "222"
    assert response.json()["reply_tweet_id"] == "0002"
    assert response.json()["screen_name"] == "david"


def test_delete_screen_name_videos_link_video_id_GOOD_USER_WRONG_VIDEO():
    response = client.delete(
        "/api/v2/users/david/videos_link/99092?tweet=false",
        headers={"Authorization": "Bearer good-token"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Videouserlink not found"}


def test_delete_screen_name_videos_link_video_id_WRONG_USER_GOOD_VIDEO():
    response = client.delete(
        "/api/v2/users/tristan/videos_link/222?tweet=false",
        headers={"Authorization": "Bearer good-token"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Videouserlink not found"}
