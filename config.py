import os


class Config(object):
    TESTING = False
    SQLALCHEMY_TRACKBACK_MODIFICATIONS = False


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/sakila'


match os.getenv('ENV'):
    case 'PRODUCTION':
        config = ProdConfig
    case _:
        config = DevConfig