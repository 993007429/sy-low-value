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

EMAIL_HOST_USER = "zhuangbaojun@ztbory.com"
EMAIL_HOST_PASSWORD = "Gang8dai"

INFLUXDB_URL = "http://192.168.0.18:8086"
INFLUXDB_ORG = "ztbr"
INFLUXDB_BUCKET = "sy-recycle"
INFLUXDB_TOKEN = "o6yW70bJO_Q-_qFg32PCIR7tKvyo_ff2aAtPXfQrO6NoKL-60VFNjba9hTXO8OE7iRXxYSaWmjXuKIhXiU8VMQ=="
