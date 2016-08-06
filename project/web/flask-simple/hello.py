#!/usr/bin/env python
# coding:utf8
import os
from flask import (
    Flask, request, make_response,
    redirect, session, flash, url_for)
from flask import render_template
from flask_script import (Manager, Shell)
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from flask_mail import (Mail, Message)
from flask_sqlalchemy import SQLAlchemy
from wtforms import (StringField, SubmitField)
from wtforms.validators import Required


app = Flask(__name__)

# smtplib mail
import sys
sys.path.append("/data/python/")
import data
# mail headers
app.config['MAIL_SERVER'] = data.MAIL_SERVER
app.config['MAIL_PORT'] = data.MAIL_PORT
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = data.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = data.MAIL_PASSWD
# mail message
app.config['MAIL_SUBJECT'] = "[bamboo web]"
app.config['MAIL_SENDER'] = data.MAIL_USERNAME
app.config['MAIL_ADMIN'] = data.MAIL_ADMIN

# sqlite db
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True


app.config['SECRET_KEY'] = "I am a secret key"
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
mail = Mail(app)
db = SQLAlchemy(app)

# DB class (ORM)
class Role(db.Model):
    """角色"""
    # 表名
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # 表明该表被某一个指定的表当为外键映射
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return "<Role {}>".format(self.name)


class User(db.Model):
    """用户名"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return "<User {}>".format(self.username)


class NameForm(Form):
    name = StringField("What is your name?",
                       validators=[Required()])
    submit = SubmitField("submit")


def send_mail(to, subject, template, **kwargs):
    msg = Message(
        app.config['MAIL_SUBJECT'] + subject,
        sender=app.config['MAIL_SENDER'],
        recipients = [to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    print msg
    mail.send(msg)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
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
            if app.config['MAIL_ADMIN']:
                send_mail(app.config['MAIL_ADMIN'],
                          "New user",
                          "mail/new_user",
                          user=user)
        else:
            session['known'] = True

        # 存储前一个输入的名称
        session['name'] = name
        if oldName and oldName != name:
            flash("Looks like you have changed your name.")

        return redirect(url_for('index'))
    return render_template(
        'index.html', user_agent=user_agent,
        form=form, name=session.get('name'),
        known=session.get('known', False)
    )


@app.route('/cookie/<name>/')
def cookie(name):
    response = make_response(
        "<h1>Hello {}, "
        "we carry a cookie!</h1>".format(name))
    response.set_cookie('answer-bamboo', '100000')
    return response


@app.route('/index.html')
def index_ref():
    return render_template('index.html')


@app.route('/user/<name>/')
def user(name):
    return render_template('user.html', name=name)


@app.route('/redirect/')
def redirect_google():
    return redirect('http://www.google.com')


# shell使用方便（避免每次启动shell都需要创建或者导入DB）
def make_shell_context():
    # 利用字典，python的自省
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()
