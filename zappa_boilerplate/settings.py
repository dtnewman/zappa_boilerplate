# -*- coding: utf-8 -*-
import os

os_env = os.environ


class Config(object):
    SECRET_KEY = os_env.get('PERSONAL_HOMEPAGE_SECRET', 'secret-key')  # used for csrf  TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 12
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class Local(Config):
    """Local configuration."""
    ENV = 'lcl'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_CONNECTION_STRING") or 'postgresql://localhost:5432/zappa_boilerplate'


class Development(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_CONNECTION_STRING") or '<DEVELOPMENT DATABASE HERE>' # TODO: Change me
    FLASKS3_ACTIVE = True
    FLASKS3_DEBUG = True


class Production(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_CONNECTION_STRING") or '<PRODUCTION DATABASE HERE>' # TODO: Change me
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class Test(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_CONNECTION_STRING") or 'postgresql://localhost:5432/zappa_boilerplate_test'
    BCRYPT_LOG_ROUNDS = 4  # For faster tests
    WTF_CSRF_ENABLED = False  # Allows form testing
