from typing import Union, List

from pydantic import BaseModel


class AdminBase(BaseModel):
    username: str


class AdminCreate(AdminBase):
    hashed_password: str


class Admin(AdminBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserBase(BaseModel):
    screen_name: str
    user_id: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserDeleted(BaseModel):
    screen_name: str
    videouserlink_deleted_count: int


class VideoBase(BaseModel):
    creator_screen_name: str
    text: str
    thumbnail_url: str
    tweet_id: str
    tweet_url: str
    creator_user_id: str
    video_url: str


class VideoCreate(VideoBase):
    pass


class Video(VideoBase):
    id: int
    is_deleted: bool

    class Config:
        orm_mode = True


class VideoDeleted(BaseModel):
    tweet_id: str
    videouserlink_deleted_count: int


class VideoUserLinkBase(BaseModel):
    tweet_id: str
    reply_tweet_id: str


class VideoUserLinkCreate(VideoUserLinkBase):
    pass


class VideoUserLink(VideoUserLinkBase):
    id: int
    screen_name: str
    asked_at: int

    class Config:
        orm_mode = True


class BannedBase(BaseModel):
    user_id: str
    reason: str


class BannedCreate(BannedBase):
    pass


class Banned(BannedBase):
    id: int
    banned_at: int

    class Config:
        orm_mode = True


class UserVideoCountScreenName(BaseModel):
    screen_name: str
    videos_count: int


class UserVideoCountTweetId(BaseModel):
    tweet_id: str
    videos_count: int


class UserVideos(BaseModel):
    screen_name: str
    videos: List
