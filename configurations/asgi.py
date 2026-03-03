import django
import os

env_state = os.getenv("ENV_STATE", "local")
if env_state == "production":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configurations.settings.production")
elif env_state == "staging":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configurations.settings.staging")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configurations.settings.local")


django.setup()

from django.core.asgi import get_asgi_application
from fastapi import FastAPI

from app.routers import auth_router, block_router, crypto_stat_router, user_router
from app.routers.health import health_router
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler


django_app = get_asgi_application()
django_app = ASGIStaticFilesHandler(django_app)
fastapi_app = FastAPI()

fastapi_app.include_router(health_router, prefix="/api", tags=["Health"])
fastapi_app.include_router(auth_router, prefix="/api", tags=["Authentication"])
fastapi_app.include_router(block_router, prefix="/api", tags=["Blocks"])
fastapi_app.include_router(crypto_stat_router, prefix="/api", tags=["Crypto Stats"])
fastapi_app.include_router(user_router, prefix="/api", tags=["Users"])


from starlette.routing import Mount
from starlette.applications import Starlette

application = Starlette(
    routes=[
        Mount("/api", app=fastapi_app),
        Mount("/", app=django_app),
    ]
)
