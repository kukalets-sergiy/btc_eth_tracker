#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser if not exists..."
echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists() or \
User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')" \
| python manage.py shell

echo "Collect static..."
python manage.py collectstatic --noinput

echo "Starting FastAPI..."
poetry run uvicorn config.asgi:fastapi_app --reload --host 0.0.0.0 --port 8000 &

echo "Starting Django ASGI..."
poetry run uvicorn config.asgi:django_app --reload --host 0.0.0.0 --port 8001

