#!/bin/sh
gunicorn -w 3 --bind 0.0.0.0:5000 wsgi:app
