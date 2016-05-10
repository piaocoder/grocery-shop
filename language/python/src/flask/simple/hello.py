#!/usr/bin/env python
# coding:utf8
from flask import (Flask, url_for,
                   render_template, request)

# 实例化Flask类，首参数为应用模块或者包名称
app = Flask(__name__)


# 告知触发什么样的URL
# 1,可选转换器：<converter:variable_name>
# 2,唯一的URL：
#       规则1：尾端是否存在/斜线，非常重要
# 3,动态URL
# 4,默认为GET方法
@app.route('/')
def hello_world():
    return 'Bamboo, Hello World!'


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/user/<username>')
def profile(username):
    # show the user profile for that user
    return 'User %s' % username


@app.route('/post/<int:post_id>')
def post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


# args属性的获取：request.args.get('q', '')
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        msg = "{0}-{1}".format(request.form['username'],
                               request.form['password'])
        print msg
    return render_template("login.html", error=error)


@app.route('/showurl')
def showurl():
    urlmsg = ''
    with app.test_request_context():
        urlmsg += url_for('login')
        urlmsg += "     "
        urlmsg += url_for('login', bamboo='/')
        urlmsg += "     "
        urlmsg += url_for('profile', username='Unlessbamboo')

    return urlmsg

if __name__ == '__main__':
    app.debug = True
    # 运行server服务器
    app.run(host='0.0.0.0')
