from twitter_bot import logger
from twitter_bot.tools.error_tools import exception

from datetime import datetime, timezone


@exception(logger)
def get_timestamp_utc() -> int:
    """Get the current timestamp utc

    Returns:
        int: utc current timestamp
    """
    dt = datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = int(utc_time.timestamp())
    return utc_timestamp


@exception(logger)
def clean_text(text: str) -> str:
    """Remove leading "@" + empty strings from text + http links

    Args:
        text (str): a text

    Returns:
        str: a cleaned text
    """
    text_split = text.split(" ")
    text_split_copy = [x for x in text_split if x]

    leading_at_removed = False
    for word in text_split:
        if word:
            if word.startswith("http"):
                text_split_copy.remove(word)
                continue

            if not leading_at_removed:
                if not word.startswith("@"):
                    leading_at_removed = True
                else:
                    text_split_copy.remove(word)

    new_text = " ".join(text_split_copy)
    return new_text
