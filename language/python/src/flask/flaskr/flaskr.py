# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

from sqlite3 import dbapi2 as sqlite3
from flask import (Flask, request, session,
                   redirect, url_for, abort,
                   render_template, flash, _app_ctx_stack)

# configuration
DATABASE = '/tmp/flaskr.db'
# 调试模式
DEBUG = True
# 安全会话
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
# 设置环境变量：Flassk_settings，指向预加载的配置文件
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def init_db():
    """Creates the database tables."""
    # 手动创建应用环境，在with语句的内部，g和app关联，之后自动销毁
    with app.app_context():
        db = get_db()
        # 打开应用提供的资源，从资源所在处打开文件并读取
        # 使用游标cursor来执行sql脚本
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
        1,config配置对象
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect(app.config['DATABASE'])
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db

    return top.sqlite_db


@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


@app.route('/')
def show_entries():
    """show_entries:显示所有的db条目"""
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    # 向下一次请求发送提示消息
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    # 如果登录失败，提示错误信息
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    # 删除会话中的提示信息
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    # 初始化数据库
    init_db()
    # 将当前文件作为一个独立应用来执行
    app.run(host='0.0.0.0')
