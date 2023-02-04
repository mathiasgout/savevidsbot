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
