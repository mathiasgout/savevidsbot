from twitter_bot.tools import twitter_tools, api_tools
from tests import overrided_dependencies, sample

from unittest.mock import ANY

import tweepy


def test_get_twitter_api(mocker):
    settings = overrided_dependencies.override_get_settings()

    # Patch de la classe "tweepy.API"
    mock_twitter_api = mocker.patch("tweepy.API")

    # Appel
    twitter_tools.get_twitter_api(settings=settings)

    # Vérification qu'on a eu un appel de la fonction "tweepy.API"
    tweepy.API.assert_called_once_with(ANY, wait_on_rate_limit=True)

    # Vérification que l'appel de tweepy.API a bien été appelé avec comme premier argument une instance
    # de la classe tweepy.auth.OAuth1UserHandler
    assert isinstance(mock_twitter_api.call_args[0][0], tweepy.auth.OAuth1UserHandler)


def test_get_status(mocker):
    settings = overrided_dependencies.override_get_settings()

    # Mock
    mocker.patch("tweepy.API.get_status", return_value="status")

    # Appel
    status = twitter_tools.get_status(settings=settings, tweet_id="111")

    # Vérification de l'appel
    tweepy.API.get_status.assert_called_once_with(id="111", tweet_mode="extended")

    # Vérification de return de 'twitter_tools.get_status'
    assert status == "status"


def test_in_reply_to_status_id_ALL_GOOD():
    status = sample.Status()

    assert twitter_tools.get_in_reply_to_status_id(status=status) == 12


def test_in_reply_to_status_id_NO_REPLY_STATUS_ID():
    status = sample.Status()
    status.in_reply_to_status_id = None

    assert twitter_tools.get_in_reply_to_status_id(status=status) is None


def test_get_video_urls_from_status_ALL_GOOD():
    status = sample.StatusComplete()

    assert twitter_tools.get_video_urls_from_status(status=status) == {
        "video_url": "good_url",
        "thumbnail_url": "thumbnail_url",
    }


def test_get_video_urls_from_status_NO_EXTENDED_ENTITIES():
    status = sample.Status()

    assert twitter_tools.get_video_urls_from_status(status=status) is None


def test_get_video_urls_from_status_NO_VIDEO_INFO():
    status = sample.StatusComplete()
    del status.extended_entities["media"][0]["video_info"]

    assert twitter_tools.get_video_urls_from_status(status=status) is None


def test_extract_infos_from_status_FULL_TEXT():
    status = sample.Status()

    assert twitter_tools.extract_infos_from_status(status=status) == {
        "tweet_id": "1",
        "user_id": "3",
        "screen_name": "didier",
        "screen_name_at": "@didier",
        "text": "lol @lod",
    }


def test_extract_infos_from_status_TEXT():
    status = sample.Status()
    status.text = "HAPPY"
    delattr(status, "full_text")

    assert twitter_tools.extract_infos_from_status(status=status) == {
        "tweet_id": "1",
        "user_id": "3",
        "screen_name": "didier",
        "screen_name_at": "@didier",
        "text": "HAPPY",
    }


def test_is_possibly_sensitive_SENSITIVE():
    status = sample.Status()
    status.possibly_sensitive = True

    assert twitter_tools.is_possibly_sensitive(status=status) is True


def test_is_possibly_sensitive_NO_SENSITIVE():
    status = sample.Status()
    status.possibly_sensitive = False

    assert twitter_tools.is_possibly_sensitive(status=status) is False


def test_is_possibly_sensitive_NO_TAG():
    status = sample.Status()

    assert twitter_tools.is_possibly_sensitive(status=status) is False


def test_post_reply_status(mocker):
    status = sample.Status()

    settings = overrided_dependencies.override_get_settings()

    # Patch
    mocker.patch("tweepy.API.update_status", return_value=status)

    # Appel
    status_id = twitter_tools.post_reply_status(
        settings=settings, text="oui", tweet_id="12"
    )

    # Vérification de l'appel
    tweepy.API.update_status.assert_called_once_with(
        status="oui", in_reply_to_status_id="12"
    )

    assert status_id == "1"


def test_handle_new_status_ALL_GOOD(mocker):
    status = sample.Status()
    in_reply_status = sample.StatusComplete()

    settings = overrided_dependencies.override_get_settings()

    # Mocks
    mocker.patch(
        "twitter_bot.tools.twitter_tools.get_status", return_value=in_reply_status
    )
    mocker.patch(
        "twitter_bot.tools.twitter_tools.get_video_urls_from_status",
        return_value={"video_url": "video_url", "thumbnail_url": "thumbnail_url"},
    )
    mocker.patch("twitter_bot.tools.api_tools.is_banned_user", return_value=False)
    mocker.patch(
        "twitter_bot.tools.api_tools.get_bearer_token", return_value="access_token"
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.create_video_if_doesnt_exist", return_value=True
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.create_user_if_doesnt_exist", return_value=True
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.get_videouserlink_by_screen_name_and_tweet_id",
        return_value=False,
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.get_video_count_by_tweet_id", return_value=0
    )
    mocker.patch(
        "twitter_bot.tools.twitter_tools.post_reply_status", return_value="100"
    )
    mocker.patch("twitter_bot.tools.api_tools.create_videouserlink", return_value=True)

    # Appel
    assert twitter_tools.handle_new_status(settings=settings, status=status) is True

    # Vérif
    twitter_tools.post_reply_status.assert_called_once_with(
        settings=settings, text="@didier Download link here! \n/2", tweet_id="1"
    )


def test_handle_new_status_NO_REPLY_IN_STATUS(mocker):
    status = sample.Status()
    status.in_reply_to_status_id = None

    settings = overrided_dependencies.override_get_settings()

    # Mocks
    mocker.patch("twitter_bot.tools.twitter_tools.get_status", return_value=None)
    mocker.patch(
        "twitter_bot.tools.twitter_tools.get_video_urls_from_status",
        return_value={"video_url": "video_url", "thumbnail_url": "thumbnail_url"},
    )
    mocker.patch("twitter_bot.tools.api_tools.is_banned_user", return_value=False)
    mocker.patch(
        "twitter_bot.tools.api_tools.get_bearer_token", return_value="access_token"
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.create_video_if_doesnt_exist", return_value=True
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.create_user_if_doesnt_exist", return_value=True
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.get_videouserlink_by_screen_name_and_tweet_id",
        return_value=False,
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.get_video_count_by_tweet_id", return_value=0
    )
    mocker.patch(
        "twitter_bot.tools.twitter_tools.post_reply_status", return_value="100"
    )
    mocker.patch("twitter_bot.tools.api_tools.create_videouserlink", return_value=True)

    assert twitter_tools.handle_new_status(settings=settings, status=status) is False

    # Verif des appels
    twitter_tools.post_reply_status.assert_not_called()


def test_handle_new_status_NO_URL(mocker):
    status = sample.Status()
    in_reply_status = sample.StatusComplete()
    del in_reply_status.extended_entities

    settings = overrided_dependencies.override_get_settings()

    # Mocks
    mocker.patch(
        "twitter_bot.tools.twitter_tools.get_status", return_value=in_reply_status
    )
    mocker.patch(
        "twitter_bot.tools.twitter_tools.get_video_urls_from_status", return_value=None
    )
    mocker.patch("twitter_bot.tools.api_tools.is_banned_user", return_value=False)
    mocker.patch(
        "twitter_bot.tools.api_tools.get_bearer_token", return_value="access_token"
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.create_video_if_doesnt_exist", return_value=True
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.create_user_if_doesnt_exist", return_value=True
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.get_videouserlink_by_screen_name_and_tweet_id",
        return_value=False,
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.get_video_count_by_tweet_id", return_value=0
    )
    mocker.patch(
        "twitter_bot.tools.twitter_tools.post_reply_status", return_value="100"
    )
    mocker.patch("twitter_bot.tools.api_tools.create_videouserlink", return_value=True)

    assert twitter_tools.handle_new_status(settings=settings, status=status) is False

    # Verif des appels
    twitter_tools.post_reply_status.assert_not_called()


def test_handle_new_status_NO_ACCESS_TOKEN(mocker):
    status = sample.Status()
    in_reply_status = sample.StatusComplete()
    del in_reply_status.extended_entities

    settings = overrided_dependencies.override_get_settings()

    # Mocks
    mocker.patch(
        "twitter_bot.tools.twitter_tools.get_status", return_value=in_reply_status
    )
    mocker.patch(
        "twitter_bot.tools.twitter_tools.get_video_urls_from_status",
        return_value={"video_url": "video_url", "thumbnail_url": "thumbnail_url"},
    )
    mocker.patch("twitter_bot.tools.api_tools.is_banned_user", return_value=False)
    mocker.patch("twitter_bot.tools.api_tools.get_bearer_token", return_value=None)
    mocker.patch(
        "twitter_bot.tools.api_tools.create_video_if_doesnt_exist", return_value=True
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.create_user_if_doesnt_exist", return_value=True
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.get_videouserlink_by_screen_name_and_tweet_id",
        return_value=False,
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.get_video_count_by_tweet_id", return_value=0
    )
    mocker.patch(
        "twitter_bot.tools.twitter_tools.post_reply_status", return_value="100"
    )
    mocker.patch("twitter_bot.tools.api_tools.create_videouserlink", return_value=True)

    assert twitter_tools.handle_new_status(settings=settings, status=status) is False

    # Verif des appels
    twitter_tools.post_reply_status.assert_not_called()


def test_handle_new_status_POSSIBLY_SENSITIVE(mocker):
    status = sample.Status()
    in_reply_status = sample.StatusComplete()
    in_reply_status.possibly_sensitive = True

    settings = overrided_dependencies.override_get_settings()

    # Mocks
    mocker.patch(
        "twitter_bot.tools.twitter_tools.get_status", return_value=in_reply_status
    )
    mocker.patch(
        "twitter_bot.tools.twitter_tools.get_video_urls_from_status",
        return_value={"video_url": "video_url", "thumbnail_url": "thumbnail_url"},
    )
    mocker.patch("twitter_bot.tools.api_tools.is_banned_user", return_value=False)
    mocker.patch(
        "twitter_bot.tools.api_tools.get_bearer_token", return_value="access_token"
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.create_video_if_doesnt_exist", return_value=True
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.create_user_if_doesnt_exist", return_value=True
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.get_videouserlink_by_screen_name_and_tweet_id",
        return_value=False,
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.get_video_count_by_tweet_id", return_value=0
    )
    mocker.patch(
        "twitter_bot.tools.twitter_tools.post_reply_status", return_value="100"
    )
    mocker.patch("twitter_bot.tools.api_tools.create_videouserlink", return_value=True)

    assert twitter_tools.handle_new_status(settings=settings, status=status) is False

    # Verif des appels
    twitter_tools.post_reply_status.assert_not_called()


def test_handle_new_status_BANNED_USER(mocker):
    status = sample.Status()
    in_reply_status = sample.StatusComplete()

    settings = overrided_dependencies.override_get_settings()

    # Mocks
    mocker.patch(
        "twitter_bot.tools.twitter_tools.get_status", return_value=in_reply_status
    )
    mocker.patch(
        "twitter_bot.tools.twitter_tools.get_video_urls_from_status",
        return_value={"video_url": "video_url", "thumbnail_url": "thumbnail_url"},
    )
    mocker.patch("twitter_bot.tools.api_tools.is_banned_user", return_value=True)
    mocker.patch(
        "twitter_bot.tools.api_tools.get_bearer_token", return_value="access_token"
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.create_video_if_doesnt_exist", return_value=True
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.create_user_if_doesnt_exist", return_value=True
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.get_videouserlink_by_screen_name_and_tweet_id",
        return_value=False,
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.get_video_count_by_tweet_id", return_value=0
    )
    mocker.patch(
        "twitter_bot.tools.twitter_tools.post_reply_status", return_value="100"
    )
    mocker.patch("twitter_bot.tools.api_tools.create_videouserlink", return_value=True)

    assert twitter_tools.handle_new_status(settings=settings, status=status) is False

    # Verif des appels
    twitter_tools.post_reply_status.assert_not_called()


def test_handle_new_status_VIDEO_IS_NOT_IN_DB_AND_CANNOT_BE_CREATED(mocker):
    status = sample.Status()
    in_reply_status = sample.StatusComplete()

    settings = overrided_dependencies.override_get_settings()

    # Mocks
    mocker.patch(
        "twitter_bot.tools.twitter_tools.get_status", return_value=in_reply_status
    )
    mocker.patch(
        "twitter_bot.tools.twitter_tools.get_video_urls_from_status",
        return_value={"video_url": "video_url", "thumbnail_url": "thumbnail_url"},
    )
    mocker.patch("twitter_bot.tools.api_tools.is_banned_user", return_value=False)
    mocker.patch(
        "twitter_bot.tools.api_tools.get_bearer_token", return_value="access_token"
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.create_video_if_doesnt_exist", return_value=False
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.create_user_if_doesnt_exist", return_value=True
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.get_videouserlink_by_screen_name_and_tweet_id",
        return_value=False,
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.get_video_count_by_tweet_id", return_value=0
    )
    mocker.patch(
        "twitter_bot.tools.twitter_tools.post_reply_status", return_value="100"
    )
    mocker.patch("twitter_bot.tools.api_tools.create_videouserlink", return_value=True)

    assert twitter_tools.handle_new_status(settings=settings, status=status) is False

    # Vérif des appels
    twitter_tools.post_reply_status.assert_not_called()


def test_handle_new_status_USER_IS_NOT_IN_DB_AND_CANNOT_BE_CREATED(mocker):
    status = sample.Status()
    in_reply_status = sample.StatusComplete()

    settings = overrided_dependencies.override_get_settings()

    # Mocks
    mocker.patch(
        "twitter_bot.tools.twitter_tools.get_status", return_value=in_reply_status
    )
    mocker.patch(
        "twitter_bot.tools.twitter_tools.get_video_urls_from_status",
        return_value={"video_url": "video_url", "thumbnail_url": "thumbnail_url"},
    )
    mocker.patch("twitter_bot.tools.api_tools.is_banned_user", return_value=False)
    mocker.patch(
        "twitter_bot.tools.api_tools.get_bearer_token", return_value="access_token"
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.create_video_if_doesnt_exist", return_value=True
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.create_user_if_doesnt_exist", return_value=False
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.get_videouserlink_by_screen_name_and_tweet_id",
        return_value=False,
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.get_video_count_by_tweet_id", return_value=0
    )
    mocker.patch(
        "twitter_bot.tools.twitter_tools.post_reply_status", return_value="100"
    )
    mocker.patch("twitter_bot.tools.api_tools.create_videouserlink", return_value=True)

    assert twitter_tools.handle_new_status(settings=settings, status=status) is False

    # Vérif des appels
    twitter_tools.post_reply_status.assert_not_called()


def test_handle_new_status_VIDEO_ALREADY_REQUESTED_BY_USER(mocker):
    status = sample.Status()
    in_reply_status = sample.StatusComplete()

    settings = overrided_dependencies.override_get_settings()

    # Mocks
    mocker.patch(
        "twitter_bot.tools.twitter_tools.get_status", return_value=in_reply_status
    )
    mocker.patch(
        "twitter_bot.tools.twitter_tools.get_video_urls_from_status",
        return_value={"video_url": "video_url", "thumbnail_url": "thumbnail_url"},
    )
    mocker.patch("twitter_bot.tools.api_tools.is_banned_user", return_value=False)
    mocker.patch(
        "twitter_bot.tools.api_tools.get_bearer_token", return_value="access_token"
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.create_video_if_doesnt_exist", return_value=True
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.create_user_if_doesnt_exist", return_value=True
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.get_videouserlink_by_screen_name_and_tweet_id",
        return_value=True,
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.get_video_count_by_tweet_id", return_value=0
    )
    mocker.patch(
        "twitter_bot.tools.twitter_tools.post_reply_status", return_value="100"
    )
    mocker.patch("twitter_bot.tools.api_tools.create_videouserlink", return_value=True)

    assert twitter_tools.handle_new_status(settings=settings, status=status) is False

    # Verif des appels
    twitter_tools.post_reply_status.assert_not_called()


def test_handle_new_status_VIDEO_REQUESTED_TOO_MANY_TIMES(mocker):
    status = sample.Status()
    in_reply_status = sample.StatusComplete()

    settings = overrided_dependencies.override_get_settings()

    # Mocks
    mocker.patch(
        "twitter_bot.tools.twitter_tools.get_status", return_value=in_reply_status
    )
    mocker.patch(
        "twitter_bot.tools.twitter_tools.get_video_urls_from_status",
        return_value={"video_url": "video_url", "thumbnail_url": "thumbnail_url"},
    )
    mocker.patch("twitter_bot.tools.api_tools.is_banned_user", return_value=False)
    mocker.patch(
        "twitter_bot.tools.api_tools.get_bearer_token", return_value="access_token"
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.create_video_if_doesnt_exist", return_value=True
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.create_user_if_doesnt_exist", return_value=True
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.get_videouserlink_by_screen_name_and_tweet_id",
        return_value=False,
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.get_video_count_by_tweet_id", return_value=10
    )
    mocker.patch(
        "twitter_bot.tools.twitter_tools.post_reply_status", return_value="100"
    )
    mocker.patch("twitter_bot.tools.api_tools.create_videouserlink", return_value=True)

    assert twitter_tools.handle_new_status(settings=settings, status=status) is False

    # Verif des appels
    twitter_tools.post_reply_status.assert_not_called()


def test_handle_new_status_LINKS_BETWEEN_USER_AND_VIDEO_NOT_CREATED(mocker):
    status = sample.Status()
    in_reply_status = sample.StatusComplete()

    settings = overrided_dependencies.override_get_settings()

    # Mocks
    mocker.patch(
        "twitter_bot.tools.twitter_tools.get_status", return_value=in_reply_status
    )
    mocker.patch(
        "twitter_bot.tools.twitter_tools.get_video_urls_from_status",
        return_value={"video_url": "video_url", "thumbnail_url": "thumbnail_url"},
    )
    mocker.patch("twitter_bot.tools.api_tools.is_banned_user", return_value=False)
    mocker.patch(
        "twitter_bot.tools.api_tools.get_bearer_token", return_value="access_token"
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.create_video_if_doesnt_exist", return_value=True
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.create_user_if_doesnt_exist", return_value=True
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.get_videouserlink_by_screen_name_and_tweet_id",
        return_value=False,
    )
    mocker.patch(
        "twitter_bot.tools.api_tools.get_video_count_by_tweet_id", return_value=0
    )
    mocker.patch(
        "twitter_bot.tools.twitter_tools.post_reply_status", return_value="100"
    )
    mocker.patch("twitter_bot.tools.api_tools.create_videouserlink", return_value=False)

    assert twitter_tools.handle_new_status(settings=settings, status=status) is True

    # Verif des appels
    twitter_tools.post_reply_status.assert_called_once_with(
        settings=settings, text="@didier Download link here! \n/2", tweet_id="1"
    )
    api_tools.create_videouserlink.assert_called_once_with(
        settings=settings,
        access_token="access_token",
        videouserlink=ANY,
        screen_name="didier",
    )
