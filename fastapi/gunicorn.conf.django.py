# WIP: for development
wsgi_app = "config.asgi:django_app"
worker_class = "uvicorn.workers.UvicornWorker"
bind = "0.0.0.0:8001"
workers = 1
daemon = False
