from . import *  # noqa

DEBUG = True

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

EMAIL_HOST_USER = "zhuangbaojun@ztbory.com"
EMAIL_HOST_PASSWORD = "Gang8dai"
