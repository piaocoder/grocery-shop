#!/usr/bin/env python
# coding:utf8
from flask import Flask, request, make_response, redirect
from flask import render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import (StringField, SubmitField)
from wtforms.validators import Required


app = Flask(__name__)
app.config['SECRET_KEY'] = "I am a secret key"
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(Form):
    name = StringField("What is your name?",
                       validators=[Required()])
    submit = SubmitField("submit")


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
        name = form.name.data
        form.name.data = ''
    return render_template(
        'index.html', user_agent=user_agent,
        form=form, name=name)


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


if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()
