#!/bin/bash
source venv/bin/activate
exec gunicorn -w 3 -b :5000 --access-logfile - --error-logfile - wsgi:app
