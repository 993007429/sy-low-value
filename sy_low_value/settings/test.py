from . import *  # noqa

DEBUG = False

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "test_sy_low_value",
        "USER": "postgres",
        "PASSWORD": "Ztbr_2022",
        "HOST": "192.168.0.18",
        "PORT": "5433",
    }
}

EMAIL_HOST = "smtp-mail.outlook.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_SENDER_NAME = "顺义再生资源"
EMAIL_HOST_USER = "ztbory@outlook.com"
EMAIL_HOST_PASSWORD = "ztbr@2022"


INFLUXDB_URL = "http://192.168.0.18:8086"
INFLUXDB_ORG = "ztbr"
INFLUXDB_BUCKET = "test-sy-recycle"
INFLUXDB_TOKEN = "m5rHB4Lzu3wyCVeHR2gDmMiPTJlGFOJfbtCg77rXrUhCgkbcz_Rt3qInJ9vvdkTpqy8IXO93wuYG7aQ1oHtRUw=="
