import logging

from django.core.management.base import BaseCommand
from django.test import override_settings

from dsbot.client import BotClient
from dsbot.conf import settings


class Command(BaseCommand):
    def add_arguments(self, parser):
        slack = parser.add_argument_group("Slack arguments")
        slack.add_argument("--token", default=settings.SLACK_TOKEN, help="Slack token")
        slack.add_argument("--timeout", default=30, type=int)
        slack.add_argument("--ping-interval", default=30, type=int)

        celery = parser.add_argument_group("Celery Arguments")
        celery.add_argument("--eager", action="store_true")

    def handle(self, verbosity, eager, **options):
        logging.root.setLevel(
            {
                0: logging.ERROR,
                1: logging.WARNING,
                2: logging.INFO,
                3: logging.DEBUG,
            }.get(verbosity)
        )

        ch = logging.StreamHandler()
        formatter = logging.Formatter(logging.BASIC_FORMAT)
        ch.setFormatter(formatter)

        logging.root.addHandler(ch)

        BotClient.load_plugins()

        with override_settings(CELERY_TASK_ALWAYS_EAGER=eager):
            BotClient(
                token=options["token"],
                timeout=options["timeout"],
                ping_interval=options["ping_interval"],
            ).start()
