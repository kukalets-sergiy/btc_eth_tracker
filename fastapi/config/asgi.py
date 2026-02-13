"""ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

"""
Settings
"""
env_state = os.getenv("ENV_STATE", "production")
if env_state == "production":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
elif env_state == "staging":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.staging")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")


"""
Django settings
"""
django_app = get_asgi_application()


"""
FastAPI settings
"""
from app.routers import auth_router, health_router, user_router, block_router, crypto_stat_router

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

fastapi_app = FastAPI()
API_PREFIX = "/api"

# routers
fastapi_app.include_router(user_router, tags=["users"], prefix=f"{API_PREFIX}/user")
fastapi_app.include_router(auth_router, tags=["auth"], prefix=f"{API_PREFIX}/auth")
fastapi_app.include_router(health_router, tags=["health"], prefix=f"{API_PREFIX}/health")
fastapi_app.include_router(block_router, tags=["block"], prefix=f"{API_PREFIX}/block")
fastapi_app.include_router(crypto_stat_router, tags=["crypto-stats"], prefix=f"{API_PREFIX}/crypto/stats")

# to mount Django
fastapi_app.mount("/django", django_app)
fastapi_app.mount("/static", StaticFiles(directory="static"), name="static")
fastapi_app.mount("/media", StaticFiles(directory="media"), name="media")
