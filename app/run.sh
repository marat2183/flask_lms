#!/bin/sh
gunicorn -w 4 --threads 2 --bind 0.0.0.0:5000 wsgi:app