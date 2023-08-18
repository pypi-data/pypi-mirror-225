from unittest import mock

from slack_sdk.web.slack_response import SlackResponse

from django.test import TestCase

from dsbot import exceptions, tasks


def mock_error(message="mock_error", **kwargs):
    kwargs.setdefault("ok", False)
    return exceptions.SlackApiError(
        message,
        SlackResponse(
            client=None,
            http_verb="POST",
            api_url="example.com",
            req_args={},
            data=kwargs,
            headers={},
            status_code=400,
        ),
    )


class TestExceptions(TestCase):
    @mock.patch("slack_sdk.web.client.WebClient.api_call")
    def test_not_in_channel(self, client: mock.MagicMock):
        with self.assertRaises(exceptions.NotInChannel):
            client.side_effect = mock_error(error="not_in_channel")
            tasks.api_call("chat.postMessage", channel="test_channel")

        with self.assertRaises(exceptions.ArchiveException):
            client.side_effect = mock_error(error="is_archived")
            tasks.api_call("chat.postMessage", channel="test_channel")

        with self.assertRaises(exceptions.ChannelNotFound):
            client.side_effect = mock_error(error="channel_not_found")
            tasks.api_call("chat.postMessage", channel="test_channel")
