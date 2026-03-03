#!/bin/bash
set -e

echo "Waiting for Postgres..."
until python manage.py migrate --check >/dev/null 2>&1; do
  sleep 2
done

python manage.py migrate
python manage.py collectstatic --noinput

exec gunicorn configurations.asgi:application \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --workers 3