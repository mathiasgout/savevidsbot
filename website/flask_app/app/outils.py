from db.firebase_db import delete_document, get_document, create_banned_document
from app import logger
from helpers.logger import exception
from twitter.outils import DeleteUserTweets

from typing import List
import datetime

from flask import abort, current_app, flash


@exception(logger)
def create_og_text(text: str) -> str:
    """Remove leading "@" and empty strings from text

    Args:
        text (str): a text

    Returns:
        str: a cleaned text
    """
    text_split = text.split(" ")
    text_split_copy = [x for x in text_split if x]
    for word in text_split:
        if word:
            if not word[0] == "@":
                break
            text_split_copy.remove(word)

    new_text = " ".join(text_split_copy)

    if not new_text:
        return "Download from SaveVidsBot"

    return new_text


@exception(logger)
def add_video_info_to_the_session(session, video_id: str) -> bool:
    """Add video information to the session

    Args:
        session (_type_): Flask session
        video_id (str): id of the video

    Returns:
        bool: True if video info added to session, False otherwise
    """
    try:
        video_document = get_document(
            collection_name=current_app.config["VIDEOS_COLLECTION"],
            document_name=video_id,
        )
    except Exception as e:
        logger.error(f"Error occured : {e}")
        abort(500)

    if video_document:
        video_url = video_document["video_url"]
        creator = video_document["screen_name"]
        tweet_url = video_document["tweet_url"]
        thumbnail_url = video_document["thumbnail_url"]
        text = create_og_text(video_document["text"])
        session["tweets"][video_id] = {
            "video_url": video_url,
            "creator": creator,
            "tweet_url": tweet_url,
            "thumbnail_url": thumbnail_url,
            "text": text,
        }
        session["avoid_tweets_issue"] = 1
        return True
    return False


@exception(logger)
def add_user_info_to_the_session(session, screen_name: str) -> bool:
    """Add user information to the session

    Args:
        session (_type_): Flask session
        screen_name (str): screen_name of the user

    Returns:
        bool: True if user info added to session, False otherwise
    """
    try:
        user_document = get_document(
            collection_name=current_app.config["USERS_COLLECTION"],
            document_name=screen_name,
        )
    except Exception as e:
        logger.error(f"Error occured : {e}")
        return abort(500)

    if user_document:
        requested_videos = [
            video["video_id"] for video in user_document["requested_videos"]
        ]
        session["users"][screen_name] = {"requested_videos": requested_videos}
        session["avoid_users_issue"] = 1
        return True
    return False


@exception(logger)
def get_user_videos(session, screen_name: str, page: int) -> List[str]:
    """Retrun list of user video ids

    Args:
        session (_type_): Flask session
        screen_name (_type_): screen_name of the user
        page (int): page number (4 videos per page)

    Returns:
       List[str]: a list of video ids
    """
    user_videos = []
    all_videos = session["users"][screen_name]["requested_videos"]
    requested_videos = all_videos[(page - 1) * current_app.config["VIDEOS_PER_PAGE"] :]
    for video_id in requested_videos:
        # If enough videos : break loop
        if len(user_videos) == current_app.config["VIDEOS_PER_PAGE"]:
            break

        # Append the video to user_video
        if video_id not in session["tweets"].keys():
            if add_video_info_to_the_session(session=session, video_id=video_id):
                user_videos.append(session["tweets"][video_id])
        else:
            user_videos.append(session["tweets"][video_id])

    return user_videos


@exception(logger)
def user_deletion(screen_name: str):
    """Delete a user and videos he asked from Firestore's collections
    Delete reply tweets from twitter

    Args:
        screen_name (str): user to ban screen_name
    """
    try:
        user_document = get_document(
            collection_name=current_app.config["USERS_COLLECTION"],
            document_name=screen_name,
        )
        if user_document:
            requested_videos = user_document["requested_videos"]
            video_ids = [d["video_id"] for d in requested_videos]
            reply_tweet_ids = [d["reply_tweet_id"] for d in requested_videos]
            user_id = user_document["user_id"]

            # Ajout de l'utilisateur dans la collection "banned"
            create_banned_document(
                collection_name=current_app.config["BANNED_COLLECTION"],
                document_name=user_id,
                screen_name=screen_name,
                user_id=user_id,
                banned_at=int(datetime.datetime.timestamp(datetime.datetime.now())),
            )

            # Suppression de toutes les vidéos qu'il a demandé de la collection "videos"
            for video_id in video_ids:
                delete_document(
                    collection_name=current_app.config["VIDEOS_COLLECTION"],
                    document_name=video_id,
                )

            # Suppression des réponses à ses tweets sur Twitter
            d = DeleteUserTweets(config=current_app.config)
            for tweet_id in reply_tweet_ids:
                d.delete_tweet(tweet_id=tweet_id)

            # Suppression du document dans la collection "users"
            delete_document(
                collection_name=current_app.config["USERS_COLLECTION"],
                document_name=screen_name,
            )

            # Flash du succès
            flash(
                f'User with screen name : "{screen_name}" banned with sucess!',
                category="sucess",
            )

        else:
            flash(
                f'User with screen name : "{screen_name}" not found!', category="error"
            )

    except Exception as e:
        logger.error(f"Error occured : {e}")
        return abort(500)


@exception(logger)
def video_deletion(video_id: str):
    """Delete a video from Firestore's collection

    Args:
        video_id (str): video ID to delete
    """
    try:
        video_document = get_document(
            collection_name=current_app.config["VIDEOS_COLLECTION"],
            document_name=video_id,
        )
        if video_document:
            video_id = video_document["tweet_id"]

            # Suppression du document
            delete_document(
                collection_name=current_app.config["VIDEOS_COLLECTION"],
                document_name=video_id,
            )
            flash(
                f'Video with ID : "{video_id}" deleted with sucess!', category="sucess"
            )

        else:
            flash(f'Video with ID : "{video_id}" not found!', category="error")

    except Exception as e:
        logger.error(f"Error occured : {e}")
        return abort(500)
