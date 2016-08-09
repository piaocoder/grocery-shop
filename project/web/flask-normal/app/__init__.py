# coding:utf8
from flask import (Flask, render_template)
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import (Mail)
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import config


# 创建扩展类实例，但是并未进行初始化
bootstrap = Bootstrap()
moment = Moment()
mail = Mail()
db = SQLAlchemy()

loginManager = LoginManager()
loginManager.session_protection = "strong"
loginManager.login_view = "auth.login"


def create_app(configName):
    """工厂函数"""
    app = Flask(__name__)
    # config
    app.config.from_object(config[configName])
    config[configName].init_app(app)

    # init extends
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    loginManager.init_app(app)

    # blue print register
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # return app object
    return app
