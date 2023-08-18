from slack_sdk.errors import SlackApiError


class BaseException(Exception):
    pass


class CommandError(BaseException):
    pass


class ArgumentError(CommandError):
    pass


# Custom slack exceptions


class ChannelError(SlackApiError):
    def __init__(self, response, **kwargs):
        self.channel = kwargs.get("channel", "Unknown")
        super().__init__(
            f"{response.data['error']} for {self.channel}",
            response,
        )


class NotInChannel(ChannelError):
    pass


class ArchiveException(ChannelError):
    pass


class ChannelNotFound(ChannelError):
    pass


# https://api.slack.com/methods/chat.postMessage#errors
channel_errors = {
    "channel_not_found": ChannelNotFound,
    "not_in_channel": NotInChannel,
    "is_archived": ArchiveException,
}


def cast_slack_exception(exception: SlackApiError, **kwargs):
    if exception.response.data["error"] in channel_errors:
        raise channel_errors[exception.response.data["error"]](
            response=exception.response, **kwargs
        ) from exception
    raise exception


class SlackException(BaseException):
    def __init__(self, response):
        self.data = response

    def __str__(self):
        return self.data["error"]

    def __repr__(self):
        return "SlackException(%s)" % self
