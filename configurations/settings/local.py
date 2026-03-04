import os
from typing import List
from .base import *


DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.getenv("POSTGRES_DB", "fastapi-django"),
        "USER": os.getenv("POSTGRES_USER", "fastapi"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "fastapi"),
        "HOST": os.getenv("POSTGRES_HOST", "postgres"),
        "PORT": os.getenv("POSTGRES_PORT", 5432),
    }
}
