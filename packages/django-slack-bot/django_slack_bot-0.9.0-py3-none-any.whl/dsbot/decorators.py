import logging
from functools import wraps

from dsbot.conf import settings

logger = logging.getLogger(__name__)


def ignore_users(ignore_user_list=settings.SLACK_IGNORE_USERS):
    def _outer(func):
        @wraps(func)
        def _inner(*args, data, **kwargs):
            if data.get("user") in ignore_user_list:
                logger.debug("Ignoring user %s", data["user"])
            else:
                return func(*args, data=data, **kwargs)

        return _inner

    return _outer


def ignore_bots(func):
    @wraps(func)
    def _inner(*args, data, **kwargs):
        subtype = data.get("subtype", "")
        if subtype not in ["bot_message", ""]:
            # https://api.slack.com/events/message/bot_message
            # We only care about bot_message or message without a subtype
            logger.debug("Skipping bot message %s", subtype)
        else:
            return func(*args, data=data, **kwargs)

    return _inner
