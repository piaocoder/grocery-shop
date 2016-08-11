# coding: utf8
from flask import (render_template, request,
                   jsonify)
from . import main


@main.app_errorhandler(403)
def forbidden(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'forbidden'})
        response.status_code = 403
        return response
    return render_template('403.html'), 403


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
