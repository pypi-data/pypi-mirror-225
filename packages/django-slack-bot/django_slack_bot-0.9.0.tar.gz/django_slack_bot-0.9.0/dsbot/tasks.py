from celery import shared_task
from slack_sdk.web.client import WebClient

from dsbot import exceptions
from dsbot.conf import settings

client = WebClient(token=settings.SLACK_TOKEN)


# Wrapped version of Slack API Calll
# We want to make it easy to rate limit our calls to slack by wrapping
# it as a shared_task.
@shared_task(rate_limit=settings.SLACK_RATE_LIMIT)
def api_call(*args, **kwargs):
    try:
        return client.api_call(*args, json=kwargs).data
    except exceptions.SlackApiError as e:
        exceptions.cast_slack_exception(e, **kwargs)
