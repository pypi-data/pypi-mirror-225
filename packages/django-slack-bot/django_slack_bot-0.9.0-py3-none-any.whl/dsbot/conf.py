from django.conf import settings as django_settings

DEFAULTS = {
    "SLACK_IGNORE_USERS": [],
    # Since we typically deploy 2 workers and we don't want to go too
    # much over the 1 message / second rate limit, we set our rate limit
    # to 0.5 to be equivilant to 1 message / 2 seconds
    # https://api.slack.com/docs/rate-limits#tier_t5
    "SLACK_RATE_LIMIT": 0.5,
}


class SettingsWrapper:
    def __getattr__(self, key):
        if key in DEFAULTS:
            return getattr(django_settings, key, DEFAULTS[key])
        return getattr(django_settings, key)


settings = SettingsWrapper()
