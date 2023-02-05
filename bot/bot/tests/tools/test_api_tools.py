from twitter_bot import schemas
from twitter_bot.tools import api_tools
from tests import overrided_dependencies
from tests import sample

import os


def test_is_banned_user_GET_200(requests_mock):
    settings = overrided_dependencies.override_get_settings()

    # On mock la requête GET et son retour
    mock_json = {"user_id": "1", "reason": "SEX", "id": 1, "banned_at": 1_000_000}
    requests_mock.get(
        os.path.join(settings.API_PREFIX, "banned", "1"),
        json=mock_json,
        status_code=200,
    )

    assert api_tools.is_banned_user(settings=settings, user_id="1") is True


def test_is_banned_user_GET_404(requests_mock):
    settings = overrided_dependencies.override_get_settings()

    # On mock la requête GET et son retour
    requests_mock.get(os.path.join(settings.API_PREFIX, "banned", "1"), status_code=404)

    assert api_tools.is_banned_user(settings=settings, user_id="1") is False


def test_create_video_if_doesnt_exist_GET_200(requests_mock):
    settings = overrided_dependencies.override_get_settings()

    # On mock les requêtes HTTP et leurs retours
    requests_mock.get(os.path.join(settings.API_PREFIX, "videos", "1"), status_code=200)

    assert (
        api_tools.create_video_if_doesnt_exist(
            settings=settings, access_token="access_token", video=sample.video_create
        )
        is True
    )


def test_create_video_if_doesnt_exist_GET_404_POST_200(requests_mock):
    settings = overrided_dependencies.override_get_settings()

    # On mock les requêtes HTTP et leurs retours
    requests_mock.get(os.path.join(settings.API_PREFIX, "videos", "1"), status_code=404)
    requests_mock.post(
        os.path.join(settings.API_PREFIX, "videos"),
        status_code=200,
        json=sample.video_in_db,
    )

    assert (
        api_tools.create_video_if_doesnt_exist(
            settings=settings, access_token="access_token", video=sample.video_create
        )
        is True
    )


def test_create_video_if_doesnt_exist_GET_404_POST_404(requests_mock):
    settings = overrided_dependencies.override_get_settings()

    # On mock les requêtes HTTP et leurs retours
    requests_mock.get(os.path.join(settings.API_PREFIX, "videos", "1"), status_code=404)
    requests_mock.post(os.path.join(settings.API_PREFIX, "videos"), status_code=404)

    assert (
        api_tools.create_video_if_doesnt_exist(
            settings=settings, access_token="access_token", video=sample.video_create
        )
        is False
    )


def test_create_user_if_doesnt_exist_GET_200(requests_mock):
    settings = overrided_dependencies.override_get_settings()

    # On mock les requêtes HTTP et leurs retours
    requests_mock.get(
        os.path.join(settings.API_PREFIX, "users", "david"), status_code=200
    )

    assert (
        api_tools.create_user_if_doesnt_exist(
            settings=settings, access_token="access_token", user=sample.user_create
        )
        is True
    )


def test_create_user_if_doesnt_exist_GET_404_POST_200(requests_mock):
    settings = overrided_dependencies.override_get_settings()

    # On mock les requêtes HTTP et leurs retours
    requests_mock.get(
        os.path.join(settings.API_PREFIX, "users", "david"), status_code=404
    )
    requests_mock.post(
        os.path.join(settings.API_PREFIX, "users"),
        status_code=200,
        json=sample.user_id_db,
    )

    assert (
        api_tools.create_user_if_doesnt_exist(
            settings=settings, access_token="access_token", user=sample.user_create
        )
        is True
    )


def test_create_user_if_doesnt_exist_GET_404_POST_404(requests_mock):
    settings = overrided_dependencies.override_get_settings()

    # On mock les requêtes HTTP et leurs retours
    requests_mock.get(
        os.path.join(settings.API_PREFIX, "users", "david"), status_code=404
    )
    requests_mock.post(os.path.join(settings.API_PREFIX, "users"), status_code=404)

    assert (
        api_tools.create_user_if_doesnt_exist(
            settings=settings, access_token="access_token", user=sample.user_create
        )
        is False
    )


def test_create_videouserlink_POST_200(requests_mock):
    settings = overrided_dependencies.override_get_settings()

    # On mock les requêtes HTTP et leurs retours
    requests_mock.post(
        os.path.join(settings.API_PREFIX, "users", "david", "videos_link"),
        status_code=200,
        json=sample.videouserlink_in_db,
    )

    assert (
        api_tools.create_videouserlink(
            settings=settings,
            access_token="access_token",
            videouserlink=sample.videouserlink_create,
            screen_name="david",
        )
        is True
    )


def test_create_videouserlink_POST_404(requests_mock):
    settings = overrided_dependencies.override_get_settings()

    # On mock les requêtes HTTP et leurs retours
    requests_mock.post(
        os.path.join(settings.API_PREFIX, "users", "david", "videos_link"),
        status_code=404,
    )

    assert (
        api_tools.create_videouserlink(
            settings=settings,
            access_token="access_token",
            videouserlink=sample.videouserlink_create,
            screen_name="david",
        )
        is False
    )


def test_get_videouserlink_by_screen_name_and_tweet_id_GET_200(requests_mock):
    settings = overrided_dependencies.override_get_settings()

    # On mock les requêtes HTTP et leurs retours
    requests_mock.get(
        os.path.join(settings.API_PREFIX, "users", "david", "videos_link", "9"),
        status_code=200,
    )

    assert (
        api_tools.get_videouserlink_by_screen_name_and_tweet_id(
            settings=settings, screen_name="david", tweet_id="9"
        )
        is True
    )


def test_get_videouserlink_by_screen_name_and_tweet_id_GET_404(requests_mock):
    settings = overrided_dependencies.override_get_settings()

    # On mock les requêtes HTTP et leurs retours
    requests_mock.get(
        os.path.join(settings.API_PREFIX, "users", "david", "videos_link", "9"),
        status_code=404,
    )

    assert (
        api_tools.get_videouserlink_by_screen_name_and_tweet_id(
            settings=settings, screen_name="david", tweet_id="9"
        )
        is False
    )


def test_get_video_count_by_tweet_id_GET_200(requests_mock):
    settings = overrided_dependencies.override_get_settings()

    # On mock les requêtes HTTP et leurs retours
    mock_json = {"tweet_id": "1", "videos_count": 1}
    requests_mock.get(
        os.path.join(settings.API_PREFIX, "videos", "1", "videos_count"),
        status_code=200,
        json=mock_json,
    )

    settings = overrided_dependencies.override_get_settings()

    assert api_tools.get_video_count_by_tweet_id(settings=settings, tweet_id="1") == 1


def test_get_video_count_by_tweet_id_GET_404(requests_mock):
    settings = overrided_dependencies.override_get_settings()

    # On mock les requêtes HTTP et leurs retours
    requests_mock.get(
        os.path.join(settings.API_PREFIX, "videos", "1", "videos_count"),
        status_code=404,
    )

    settings = overrided_dependencies.override_get_settings()

    assert (
        api_tools.get_video_count_by_tweet_id(settings=settings, tweet_id="1") is None
    )


def test_get_bearer_token_POST_200(requests_mock):
    settings = overrided_dependencies.override_get_settings()

    # On mock les requêtes HTTP et leurs retours
    mock_json = {"access_token": "access_token", "token_type": "bearer"}
    requests_mock.post(
        os.path.join(settings.API_PREFIX, "auth", "login"),
        status_code=200,
        json=mock_json,
    )

    assert api_tools.get_bearer_token(settings=settings) == "access_token"


def test_get_bearer_token_POST_401(requests_mock):
    settings = overrided_dependencies.override_get_settings()

    # On mock les requêtes HTTP et leurs retours
    requests_mock.post(
        os.path.join(settings.API_PREFIX, "auth", "login"), status_code=401
    )

    assert api_tools.get_bearer_token(settings=settings) is None
