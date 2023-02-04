from api.tools import twitter_tools
from tests import overrided_dependencies

import tweepy
from unittest.mock import ANY


def test_get_twitter_api(mocker):
    settings = overrided_dependencies.override_get_settings()

    # Patch de la classe "tweepy.API"
    mock_twitter_api = mocker.patch("tweepy.API")
    twitter_tools.get_twitter_api(settings=settings)

    # Vérification qu'on a eu un appel de la fonction "tweepy.API"
    tweepy.API.assert_called_once_with(ANY, wait_on_rate_limit=True)

    # Vérification que l'appel de tweepy.API a bien été appelé avec comme premier argument une instance
    # de la classe tweepy.auth.OAuth1UserHandler
    assert isinstance(mock_twitter_api.call_args[0][0], tweepy.auth.OAuth1UserHandler)


def test_delete_tweet(mocker):
    settings = overrided_dependencies.override_get_settings()

    # Patch de la fonction "tweepy.API.destroy_status"
    mock_destroy_status = mocker.patch("tweepy.API.destroy_status")
    twitter_tools.delete_tweet(settings=settings, tweet_id="1")

    # Vérification qu'on a eu un appel de la fonction "tweepy.API.destroy_status"
    tweepy.API.destroy_status.assert_called_once_with(id="1")
