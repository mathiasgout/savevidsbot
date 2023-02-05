from twitter_bot import schemas


class Status:
    def __init__(self) -> None:
        self.id = 1
        self.in_reply_to_status_id = 12
        self.full_text = "@tol http:// lol @lod"
        self.user = self.User()

    class User:
        def __init__(self) -> None:
            self.id = 3
            self.screen_name = "didier"


class StatusComplete:
    def __init__(self) -> None:
        self.id = 2
        self.full_text = "fsllfd"
        self.user = self.User()
        self.extended_entities = {
            "media": [
                {
                    "media_url_https": "thumbnail_url",
                    "video_info": {
                        "variants": [
                            {"bitrate": 10000, "url": "good_url"},
                            {"bitrate": 5000, "url": "bad_url"},
                        ]
                    },
                }
            ]
        }

    class User:
        def __init__(self) -> None:
            self.id = 4
            self.screen_name = "jeannot"


video_create = schemas.VideoCreate(
    creator_screen_name="creator_screen_name",
    text="text",
    thumbnail_url="thumbnail_url",
    tweet_id="1",
    tweet_url="tweet_url",
    creator_user_id="2",
    video_url="video_url",
)
video_in_db = video_create.dict()
video_in_db["id"] = 1
video_in_db["is_deleted"] = False

user_create = schemas.UserCreate(screen_name="david", user_id="2")
user_id_db = user_create.dict()
user_id_db["id"] = 1


videouserlink_create = schemas.VideoUserLinkCreate(tweet_id="9", reply_tweet_id="11")
videouserlink_in_db = videouserlink_create.dict()
videouserlink_in_db["id"] = 1
videouserlink_in_db["screen_name"] = "david"
videouserlink_in_db["asked_at"] = 1_000_000
