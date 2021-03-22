import os
import redis

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)

    DB_NAME = os.environ.get('DB_NAME')
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
    DB_PORT = os.environ.get('DB_PORT', 27017)

    MONGODB_SETTINGS = {
        'db': DB_NAME,
        'username': DB_USERNAME,
        'password': DB_PASSWORD,
        'host': DB_HOST,
        'port': DB_PORT
    }

    REDIS_HOST = os.environ.get('REDIS_HOST') or '127.0.0.1'
    REDIS_PORT = os.environ.get('REDIS_PORT') or 6379
    REDIS_USER = os.environ.get('REDIS_USER')
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')

    SESSION_REDIS = redis.Redis(
        REDIS_HOST,
        REDIS_PORT,
        username=REDIS_USER,
        password=REDIS_PASSWORD
    )

    SESSION_TYPE = os.environ.get('SESSION_TYPE', 'filesystem')
    SESSION_PERMANENT = os.environ.get('SESSION_PERMANENT', False)
    SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME', 'docker/flask')
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', False)
    # PERMANENT_SESSION_LIFETIME = os.environ.get('PERMANENT_SESSION_LIFETIME', 60*60*24*7)

    AZURE_CLIENT_ID = os.environ.get('AZURE_CLIENT_ID')
    AZURE_CLIENT_SECRET = os.environ.get('AZURE_CLIENT_SECRET')
    AZURE_TENANT_NAME = os.environ.get('AZURE_TENANT_NAME')
    AZURE_TENANT_ID = os.environ.get('AZURE_TENANT_ID')

    AZURE_API_BASE_URL = os.environ.get('AZURE_API_BASE_URL') or 'https://graph.microsoft.com/v1.0/'

    # Flask-User settings
    USER_APP_NAME = "Flask-LMS"  # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False  # Disable email authentication
    USER_ENABLE_USERNAME = True  # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = True  # Simplify register form


