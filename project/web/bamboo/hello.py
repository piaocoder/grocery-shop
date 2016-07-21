#!/usr/bin/env python
# coding:utf8
from flask import Flask, request, make_response, redirect
from flask import render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return render_template(
        'index.html', user_agent=user_agent)


@app.route('/cookie/<name>/')
def cookie(name):
    response = make_response(
        "<h1>Hello {}, "
        "we carry a cookie!</h1>".format(name))
    response.set_cookie('answer-bamboo', '100000')
    return response


@app.route('/user/<name>/')
def user(name):
    if name is not "bamboo":
        return render_template('user.html')
    else:
        return render_template('user.html', name=name)


@app.route('/redirect/')
def redirect_google():
    return redirect('http://www.google.com')


if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()
