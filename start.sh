#!/usr/bin/env bash

python3 manage.py migrate
python3 manage.py collectstatic --noinput
gunicorn --bind 0.0.0.0:8000 --reload api.wsgi:application
