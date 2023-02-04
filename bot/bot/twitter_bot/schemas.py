from dataclasses import dataclass, asdict


@dataclass
class UserCreate:
    screen_name: str
    user_id: str

    def dict(self):
        return {key: value for key, value in asdict(self).items()}


@dataclass
class VideoCreate:
    creator_screen_name: str
    text: str
    thumbnail_url: str
    tweet_id: str
    tweet_url: str
    creator_user_id: str
    video_url: str

    def dict(self):
        return {key: value for key, value in asdict(self).items()}


@dataclass
class VideoUserLinkCreate:
    tweet_id: str
    reply_tweet_id: str

    def dict(self):
        return {key: value for key, value in asdict(self).items()}
