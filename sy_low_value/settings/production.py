import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from . import *  # noqa

DEBUG = False
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "sy_low_value",
        "USER": "postgres",
        "PASSWORD": "Ztbr_2022",
        "HOST": "192.168.0.18",
        "PORT": "5433",
    }
}


sentry_sdk.init(
    dsn="http://c3b17646c4534ae3b0808f66e1231287@sentry.ztbory.com/18",
    integrations=[DjangoIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=0.1,
)

JWT_EXPIRE = 60 * 60 * 24 * 1

MINI_APP_ID = "wx0f9115bab5e083be"
MINI_APP_SECRET = "b5368dc0050417e60323746ca5a6b9f8"
