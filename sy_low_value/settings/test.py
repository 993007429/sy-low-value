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

JWT_EXPIRE = 60 * 60 * 24 * 1

MINI_APP_ID = "wx0f9115bab5e083be"
MINI_APP_SECRET = "b5368dc0050417e60323746ca5a6b9f8"
