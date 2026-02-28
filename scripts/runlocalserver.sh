#!/bin/bash
set -e

echo "Waiting for Postgres..."
until python manage.py showmigrations >/dev/null 2>&1; do
  sleep 2
done

echo "Running migrations..."
python manage.py makemigrations --noinput
echo "Waiting for migrations to be ready..."
until python manage.py makemigrations --check --noinput >/dev/null 2>&1; do
  sleep 2
done
python manage.py migrate

echo "Creating superuser if not exists..."
echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists() or \
User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')" \
| python manage.py shell

echo "Starting Server..."
poetry run uvicorn configurations.asgi:application --host 0.0.0.0 --port 8000 --reload
