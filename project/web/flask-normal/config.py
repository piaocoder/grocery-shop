# coding:utf8
import os
import sys


# 注意该文件夹中存放了下面的很多全局变量信息
baseDir = os.path.abspath(os.path.dirname(__file__))
sys.path.append("/data/python/")
import webenv


class Config:
    # key
    SECRET_KEY = "I am a secret key"

    # sql
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # email
    MAIL_SENDER = webenv.MAIL_USERNAME
    MAIL_ADMIN = webenv.MAIL_ADMIN
    MAIL_SERVER = webenv.MAIL_SERVER
    MAIL_PORT = webenv.MAIL_PORT
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = webenv.MAIL_USERNAME
    MAIL_PASSWORD = webenv.MAIL_PASSWD
    MAIL_SUBJECT = "[bamboo web]"
    # pages
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """开发模式"""
    DEBUG = True
    # sql
    SQLALCHEMY_DATABASE_URI = webenv.DEV_DATABASE_URL or \
        'sqlite:///' + os.path.join(
            baseDir, 'db/data-dev.sqlite')


class TestingConfig(Config):
    """测试模式"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = webenv.TEST_DATABASE_URL or \
        'sqlite:///' + os.path.join(
            baseDir, 'db/data-test.sqlite')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """生产模式"""
    SQLALCHEMY_DATABASE_URI = webenv.DATABASE_URL or \
        'sqlite:///' + os.path.join(
            baseDir, 'db/data.sqlite')


config = {
    "development":  DevelopmentConfig,
    "testing":      TestingConfig,
    "production":   ProductionConfig,

    "default":      DevelopmentConfig,
}
