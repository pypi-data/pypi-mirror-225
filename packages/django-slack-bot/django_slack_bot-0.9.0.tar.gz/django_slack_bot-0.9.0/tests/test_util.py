from django.test import TestCase

from dsbot import util


class TestUtilPackage(TestCase):
    def test_parse(self):
        result = util.parse_links(
            """
        Test Text
        <https://example.com?one=1&amp;two=2>\r\n<https://another.example.com>
        Again
        """
        )
        self.assertEqual(
            list(result),
            ["https://example.com?one=1&two=2", "https://another.example.com"],
        )

    def test_direct_message(self):
        not_a_mention = "This is not a mention"
        result = util.parse_direct_mention(not_a_mention)
        self.assertEqual(result, (None, None))

        cc_mention = "CC <@Usomehting>"
        result = util.parse_direct_mention(cc_mention)
        self.assertEqual(result, (None, None))

        direct_mention = "<@Usomehting> Check this out"
        result = util.parse_direct_mention(direct_mention)
        self.assertEqual(result, ("Usomehting", "Check this out"))
