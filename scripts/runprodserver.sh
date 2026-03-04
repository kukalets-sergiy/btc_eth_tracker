#!/bin/sh
set -e

echo "Waiting for Postgres...!"
until python manage.py showmigrations >/dev/null 2>&1; do
  sleep 2
done

echo "Running migrations..."
python manage.py migrate --noinput

echo "Fixing permissions..."
chown -R app:app /home/app/staticfiles /home/app/mediafiles
python manage.py collectstatic --noinput
echo "Starting Server..."

exec gunicorn configurations.asgi:application \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --workers 3