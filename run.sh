#!/bin/bash
source venv/bin/activate
exec venv/bin/gunicorn -w 3 -b ":${PORT:5000}" --access-logfile - --error-logfile - wsgi:app
