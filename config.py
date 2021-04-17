import os
import redis

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    FLASK_ADMIN_SWATCH = 'pulse'
    MONGO_DB = os.environ.get('MONGO_DB')
    MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
    MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
    MONGO_HOST = os.environ.get('MONGO_HOST')
    MONGO_PORT = int(os.environ.get('MONGO_PORT')) or 27017

    MONGO_URI = 'mongodb+srv://{}:{}@{}:{}/{}'.format(
        MONGO_USERNAME,
        MONGO_PASSWORD,
        MONGO_HOST,
        MONGO_PORT,
        MONGO_DB
    )

    MONGODB_SETTINGS = {
        'db': MONGO_DB,
        'username': MONGO_USERNAME,
        'password': MONGO_PASSWORD,
        'host': MONGO_HOST,
        'port': MONGO_PORT
    }

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

    AZURE_CLIENT_ID = os.environ.get('AZURE_CLIENT_ID')
    AZURE_CLIENT_SECRET = os.environ.get('AZURE_CLIENT_SECRET')
    AZURE_TENANT_NAME = os.environ.get('AZURE_TENANT_NAME')
    AZURE_TENANT_ID = os.environ.get('AZURE_TENANT_ID')
    AZURE_API_BASE_URL = os.environ.get('AZURE_API_BASE_URL') or 'https://graph.microsoft.com/v1.0/'

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


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,
    'unix': UnixConfig,
    'default': DevelopmentConfig
}
