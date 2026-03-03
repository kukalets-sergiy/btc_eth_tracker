import os
from typing import List
from .base import *


DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.getenv("DB_NAME", "fastapi-django"),
        "USER": os.getenv("DB_USER", "fastapi"),
        "PASSWORD": os.getenv("DB_PASSWORD", "fastapi"),
        "HOST": os.getenv("DB_HOST", "postgres"),
        "PORT": os.getenv("DB_PORT", 5432),
    }
}
