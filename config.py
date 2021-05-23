import os
import redis
from urllib.parse import urlparse

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)

    FLASK_ADMIN_SWATCH = 'pulse'
    FLASK_ADMIN_FLUID_LAYOUT = True

    MONGO_DB = os.environ.get('MONGO_DB')
    MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
    MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
    MONGO_HOST = os.environ.get('MONGO_HOST')
    MONGO_PORT = int(os.environ.get('MONGO_PORT')) or 27017

    MONGO_URI = os.environ.get('MONGO_URI')

    if MONGO_URI is not None:
        uri = urlparse(MONGO_URI)
        MONGO_HOST = uri.hostname
        MONGO_PORT = int(uri.port)
        MONGO_USERNAME = uri.username
        MONGO_PASSWORD = uri.password


    MONGODB_SETTINGS = {
        'uri': MONGO_URI,
        'db': MONGO_DB,
        'username': MONGO_USERNAME,
        'password': MONGO_PASSWORD,
        'host': MONGO_HOST,
        'port': MONGO_PORT
    }

    REDIS_URL = os.environ.get('REDIS_URL')
    if REDIS_URL is not None:
        SESION_REDIS = redis.from_url(REDIS_URL)
    else:
        REDIS_HOST = os.environ.get('REDIS_HOST')
        REDIS_PORT =  int(os.environ.get('REDIS_PORT')) or 6379
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
    SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME', 'flask')
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', False)
    # PERMANENT_SESSION_LIFETIME = os.environ.get('PERMANENT_SESSION_LIFETIME', 60*60*24*7)

    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')

    AZURE_CLIENT_ID = os.environ.get('AZURE_CLIENT_ID')
    AZURE_CLIENT_SECRET = os.environ.get('AZURE_CLIENT_SECRET')
    AZURE_TENANT_NAME = os.environ.get('AZURE_TENANT_NAME')
    AZURE_TENANT_ID = os.environ.get('AZURE_TENANT_ID')
    AZURE_API_BASE_URL = os.environ.get('AZURE_API_BASE_URL') or 'https://graph.microsoft.com/v1.0/'

    ICTIS_API_URL = os.environ.get('ICTIS_API_URL')
    ICTIS_API_LOGIN = os.environ.get('ICTIS_API_LOGIN')
    ICITS_API_PASSWORD = os.environ.get('ICITS_API_PASSWORD')

    @classmethod
    def init_app(cls, app):
        pass


class TestingConfig(Config):
    TESTING = True
    DEBUG = True

    @classmethod
    def init_app(cls, app):
        pass

class ProductionConfig(Config):
    @classmethod
    def init_app(cls, app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.INFO)
        app.logger.addHandler(syslog_handler)


class DockerConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

class HerokuConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,
    'heroku': HerokuConfig,
    'unix': UnixConfig,
    'default': DevelopmentConfig
}
