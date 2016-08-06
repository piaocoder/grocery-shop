# coding:utf8
from datetime import datetime
from flask import (render_template, session,
                   redirect, url_for, request,
                   current_app, flash)

from . import main
from .forms import NameForm
from .. import db
from ..email import send_mail
from ..models import (Role, User)


@main.route('/', methods=['GET', 'POST'])
def index():
    user_agent = request.headers.get('User-Agent')
    name = None
    form = NameForm()
    if form.validate_on_submit():
        # 获取前一个输入的名称
        oldName = session.get('name')

        # 数据库操作
        name = form.name.data
        user = User.query.filter_by(username=name).first()
        if user is None:
            user = User(username=name)
            db.session.add(user)
            session['known'] = False
            if current_app.config['MAIL_ADMIN']:
                send_mail(
                    current_app.config['MAIL_ADMIN'],
                    "New user", "mail/new_user",
                    user=user)
        else:
            session['known'] = True

        # 存储前一个输入的名称
        session['name'] = name
        if oldName and oldName != name:
            flash("Looks like you have changed your name.")

        # 蓝本中的不同地方
        return redirect(url_for('.index'))
    return render_template(
        'index.html', user_agent=user_agent,
        form=form, name=session.get('name'),
        known=session.get('known', False)
    )


@main.route('/cookie/<name>/')
def cookie(name):
    response = make_response(
        "<h1>Hello {}, "
        "we carry a cookie!</h1>".format(name))
    response.set_cookie('answer-bamboo', '100000')
    return response


@main.route('/index.html')
def index_ref():
    return render_template('index.html')


@main.route('/user/<name>/')
def user(name):
    return render_template('user.html', name=name)


@main.route('/redirect/')
def redirect_google():
    return redirect('http://www.google.com')
