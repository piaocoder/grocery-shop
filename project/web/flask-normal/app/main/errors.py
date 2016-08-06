# coding: utf8
from flask import render_template
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    """page_not_found:全局的错误处理程序，
        不能使用app.errorhandler来wrap

    :param e:
    """
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    """internal_server_error:500

    :param e:
    """
    return render_template('500.html'), 500
