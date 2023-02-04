from api import schemas
from api.crud import (
    crud_users,
    crud_videos,
    crud_videouserlinks,
    crud_misc,
    crud_banned,
)

import os
import time

from sqlalchemy import create_engine


DATABASE_URL = os.path.join(os.path.dirname(os.path.realpath(__file__)), "db_test.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_URL}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


def create_sample_dataset(db):
    """Create sample dataset

    Args:
        db (Session): DB session
    """
    crud_users.create_user(
        db=db, user=schemas.UserCreate(screen_name="david", user_id="1")
    )  # id=1
    crud_users.create_user(
        db=db, user=schemas.UserCreate(screen_name="joseph", user_id="2")
    )  # id=2
    crud_users.create_user(
        db=db, user=schemas.UserCreate(screen_name="charles", user_id="2")
    )  # id=3
    crud_users.create_user(
        db=db, user=schemas.UserCreate(screen_name="olivier", user_id="3")
    )  # id=4
    crud_users.create_user(
        db=db, user=schemas.UserCreate(screen_name="gauthier", user_id="4")
    )  # id=5

    crud_banned.create_banned(
        db=db, banned=schemas.BannedCreate(user_id="4", reason="SEX")
    )

    crud_videos.create_video(
        db=db,
        video=schemas.VideoCreate(
            creator_screen_name="creator_screen_name",
            text="text",
            thumbnail_url="https://thumbnail_url.com",
            tweet_id="111",
            tweet_url="https://tweet_url.com",
            creator_user_id="111",
            video_url="https://video_url.com",
        ),
    )  # id=1

    crud_videos.create_video(
        db=db,
        video=schemas.VideoCreate(
            creator_screen_name="creator_screen_name2",
            text="text2",
            thumbnail_url="https://thumbnail_url.com2",
            tweet_id="222",
            tweet_url="https://tweet_url.com2",
            creator_user_id="222",
            video_url="https://video_url.com2",
        ),
    )  # id=2

    crud_videos.create_video(
        db=db,
        video=schemas.VideoCreate(
            creator_screen_name="creator_screen_name3",
            text="text3",
            thumbnail_url="https://thumbnail_url.com3",
            tweet_id="333",
            tweet_url="https://tweet_url.com3",
            creator_user_id="333",
            video_url="https://video_url.com3",
        ),
    )  # id=3

    crud_videos.create_video(
        db=db,
        video=schemas.VideoCreate(
            creator_screen_name="creator_screen_name4",
            text="text4",
            thumbnail_url="https://thumbnail_url.com4",
            tweet_id="444",
            tweet_url="https://tweet_url.com4",
            creator_user_id="444",
            video_url="https://video_url.com4",
        ),
    )  # id=3

    crud_videouserlinks.create_videouserlink(
        db=db,
        videouserlink=schemas.VideoUserLinkCreate(
            tweet_id="111", reply_tweet_id="0001"
        ),
        screen_name="david",
    )  # id=1

    time.sleep(1.5)
    crud_videouserlinks.create_videouserlink(
        db=db,
        videouserlink=schemas.VideoUserLinkCreate(
            tweet_id="222", reply_tweet_id="0002"
        ),
        screen_name="david",
    )  # id=2

    time.sleep(1.5)
    crud_videouserlinks.create_videouserlink(
        db=db,
        videouserlink=schemas.VideoUserLinkCreate(
            tweet_id="333", reply_tweet_id="0003"
        ),
        screen_name="david",
    )  # id=3

    crud_videouserlinks.create_videouserlink(
        db=db,
        videouserlink=schemas.VideoUserLinkCreate(
            tweet_id="111", reply_tweet_id="0004"
        ),
        screen_name="joseph",
    )  # id=4

    time.sleep(1.5)
    crud_videouserlinks.create_videouserlink(
        db=db,
        videouserlink=schemas.VideoUserLinkCreate(
            tweet_id="111", reply_tweet_id="0005"
        ),
        screen_name="charles",
    )  # id=5


def delete_sample_dataset(db):
    """Delete sample dataset

    Args:
        db (Session): DB session
    """
    crud_misc.delete_all_rows_of_table(db=db, table_name="VideoUserLink")
    crud_misc.delete_all_rows_of_table(db=db, table_name="User")
    crud_misc.delete_all_rows_of_table(db=db, table_name="Video")
    crud_misc.delete_all_rows_of_table(db=db, table_name="Banned")
    crud_misc.delete_all_rows_of_table(db=db, table_name="Admin")
