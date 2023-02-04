from twitter_bot import schemas
from twitter_bot.tools import api_tools
from tests import overrided_dependencies


def test_is_banned_user_GET_200(mocker):
    mock_get_request = mocker.patch("requests.get")
    mock_get_request.return_value.status_code = 200

    settings = overrided_dependencies.override_get_settings()

    assert api_tools.is_banned_user(settings=settings, user_id="1") is True


def test_is_banned_user_GET_404(mocker):
    mock_get_request = mocker.patch("requests.get")
    mock_get_request.return_value.status_code = 404

    settings = overrided_dependencies.override_get_settings()

    assert api_tools.is_banned_user(settings=settings, user_id="1") is False


def test_create_video_if_doesnt_exist_GET_200(mocker):
    mock_get_request = mocker.patch("requests.get")
    mock_get_request.return_value.status_code = 200

    settings = overrided_dependencies.override_get_settings()

    assert (
        api_tools.create_video_if_doesnt_exist(
            settings=settings,
            video=schemas.VideoCreate(
                creator_screen_name="creator_screen_name",
                text="text",
                thumbnail_url="thumbnail_url",
                tweet_id="1",
                tweet_url="tweet_url",
                creator_user_id="2",
                video_url="video_url",
            ),
        )
        is True
    )


def test_create_video_if_doesnt_exist_GET_404_POST_200(mocker):
    mock_get_request = mocker.patch("requests.get")
    mock_get_request.return_value.status_code = 404
    mock_post_request = mocker.patch("requests.post")
    mock_post_request.return_value.status_code = 200

    settings = overrided_dependencies.override_get_settings()

    assert (
        api_tools.create_video_if_doesnt_exist(
            settings=settings,
            video=schemas.VideoCreate(
                creator_screen_name="creator_screen_name",
                text="text",
                thumbnail_url="thumbnail_url",
                tweet_id="1",
                tweet_url="tweet_url",
                creator_user_id="2",
                video_url="video_url",
            ),
        )
        is True
    )


def test_create_video_if_doesnt_exist_GET_404_POST_404(mocker):
    mock_get_request = mocker.patch("requests.get")
    mock_get_request.return_value.status_code = 404
    mock_post_request = mocker.patch("requests.post")
    mock_post_request.return_value.status_code = 404

    settings = overrided_dependencies.override_get_settings()

    assert (
        api_tools.create_video_if_doesnt_exist(
            settings=settings,
            video=schemas.VideoCreate(
                creator_screen_name="creator_screen_name",
                text="text",
                thumbnail_url="thumbnail_url",
                tweet_id="1",
                tweet_url="tweet_url",
                creator_user_id="2",
                video_url="video_url",
            ),
        )
        is False
    )


def test_create_user_if_doesnt_exist_GET_200(mocker):
    mock_get_request = mocker.patch("requests.get")
    mock_get_request.return_value.status_code = 200

    settings = overrided_dependencies.override_get_settings()

    assert (
        api_tools.create_user_if_doesnt_exist(
            settings=settings, user=schemas.UserCreate(screen_name="david", user_id="2")
        )
        is True
    )


def test_create_user_if_doesnt_exist_GET_404_POST_200(mocker):
    mock_get_request = mocker.patch("requests.get")
    mock_get_request.return_value.status_code = 404
    mock_post_request = mocker.patch("requests.post")
    mock_post_request.return_value.status_code = 200

    settings = overrided_dependencies.override_get_settings()

    assert (
        api_tools.create_user_if_doesnt_exist(
            settings=settings, user=schemas.UserCreate(screen_name="david", user_id="2")
        )
        is True
    )


def test_create_user_if_doesnt_exist_GET_404_POST_404(mocker):
    mock_get_request = mocker.patch("requests.get")
    mock_get_request.return_value.status_code = 404
    mock_post_request = mocker.patch("requests.post")
    mock_post_request.return_value.status_code = 404

    settings = overrided_dependencies.override_get_settings()

    assert (
        api_tools.create_user_if_doesnt_exist(
            settings=settings, user=schemas.UserCreate(screen_name="david", user_id="2")
        )
        is False
    )


def test_create_videouserlink_POST_200(mocker):
    mock_post_request = mocker.patch("requests.post")
    mock_post_request.return_value.status_code = 200

    settings = overrided_dependencies.override_get_settings()

    assert (
        api_tools.create_videouserlink(
            settings=settings,
            videouserlink=schemas.VideoUserLinkCreate(
                tweet_id="9", reply_tweet_id="11"
            ),
            screen_name="david",
        )
        is True
    )


def test_create_videouserlink_POST_404(mocker):
    mock_post_request = mocker.patch("requests.post")
    mock_post_request.return_value.status_code = 404

    settings = overrided_dependencies.override_get_settings()

    assert (
        api_tools.create_videouserlink(
            settings=settings,
            videouserlink=schemas.VideoUserLinkCreate(
                tweet_id="9", reply_tweet_id="11"
            ),
            screen_name="david",
        )
        is False
    )


def test_get_videouserlink_by_screen_name_and_tweet_id_GET_200(mocker):
    mock_get_request = mocker.patch("requests.get")
    mock_get_request.return_value.status_code = 200

    settings = overrided_dependencies.override_get_settings()

    assert (
        api_tools.get_videouserlink_by_screen_name_and_tweet_id(
            settings=settings, screen_name="david", tweet_id="1"
        )
        is True
    )


def test_get_videouserlink_by_screen_name_and_tweet_id_GET_404(mocker):
    mock_get_request = mocker.patch("requests.get")
    mock_get_request.return_value.status_code = 404

    settings = overrided_dependencies.override_get_settings()

    assert (
        api_tools.get_videouserlink_by_screen_name_and_tweet_id(
            settings=settings, screen_name="david", tweet_id="1"
        )
        is False
    )


def test_get_video_count_by_tweet_id_GET_200(mocker):
    mock_get_request = mocker.patch("requests.get")
    mock_get_request.return_value.status_code = 200
    mock_get_request.return_value.json.return_value = {
        "videos_count": 1
    }  # Pour initialiser le response.json()

    settings = overrided_dependencies.override_get_settings()

    assert api_tools.get_video_count_by_tweet_id(settings=settings, tweet_id="1") == 1


def test_get_video_count_by_tweet_id_GET_404(mocker):
    mock_get_request = mocker.patch("requests.get")
    mock_get_request.return_value.status_code = 404

    settings = overrided_dependencies.override_get_settings()

    assert (
        api_tools.get_video_count_by_tweet_id(settings=settings, tweet_id="1") is None
    )
