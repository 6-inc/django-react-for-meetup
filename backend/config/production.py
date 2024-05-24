from .settings import *  # base.pyを読み込む
import os

# 開発、本番で分けたい設定を記載

DEBUG = False

DOMAIN = "xxxxxxxxx.com"

ALLOWED_HOSTS = ["api.xxxxxxxxx.com"]

CORS_ALLOWED_ORIGINS = [
    "https://xxxxxxxxx.com/",
]
CORS_ORIGIN_WHITELIST = ["https://xxxxxxxxx.com"]

STATIC_ROOT = os.path.join(BASE_DIR, "../static")
MEDIA_ROOT = os.path.join(BASE_DIR, "../media")


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("DATABASE_NAME"),
        "USER": config("DATABASE_USER"),
        "PASSWORD": config("DATABASE_PASSWORD"),
        "HOST": config("DATABASE_HOST"),
        "PORT": "3306",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


