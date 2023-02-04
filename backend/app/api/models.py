from api.database import Base
from api.tools import basic_tools

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    screen_name = Column(String(30), unique=True)
    user_id = Column(String)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, screen_name='{self.screen_name}', user_id='{self.user_id}')>"


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True)
    creator_screen_name = Column(String(30))
    text = Column(String)
    thumbnail_url = Column(String)
    tweet_id = Column(String, unique=True)
    tweet_url = Column(String, unique=True)
    creator_user_id = Column(String)
    video_url = Column(String)
    is_deleted = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"<Video(id={self.id}, tweet_id='{self.tweet_id}', creator_screen_name='{self.creator_screen_name}')>"


class VideoUserLink(Base):
    __tablename__ = "videos_users_link"

    id = Column(Integer, primary_key=True)
    screen_name = Column(String(30), ForeignKey("users.screen_name"))
    tweet_id = Column(String, ForeignKey("videos.tweet_id"))
    reply_tweet_id = Column(String, unique=True)
    asked_at = Column(Integer, default=basic_tools.get_timestamp_utc)

    def __repr__(self) -> str:
        return f"<VideoUserLink(id={self.id}, tweet_id='{self.tweet_id}', screen_name='{self.screen_name}')>"


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    hashed_password = Column(String)

    def __repr__(self) -> str:
        return f"<Admin(id={self.id}, username='{self.username}')>"


class Banned(Base):
    __tablename__ = "banned"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True)
    banned_at = Column(Integer, default=basic_tools.get_timestamp_utc)
    reason = Column(String(15))

    def __repr__(self) -> str:
        return (
            f"<Banned(id={self.id}, user_id='{self.user_id}', reason='{self.reason}')>"
        )
