#!/bin/sh
gunicorn -w 5 --threads 2 --bind 0.0.0.0:5000 app:create_app()
