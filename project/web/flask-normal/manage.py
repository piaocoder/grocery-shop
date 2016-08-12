#!/usr/bin/env python
# coding:utf8
import os
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

from app import create_app, db
from app.models import (Role, User, Post)
from flask_script import (Manager, Shell)
from flask_migrate import (Migrate, MigrateCommand)


app = create_app(os.getenv("FLASK_CONFIG") or "default")
manager = Manager(app)
migrate = Migrate(app, db)


@manager.command
def test(coverage=False):
    """test:Run the unit test
        shell command：
            python manager.py test
    """
    # 1, fork子进程，重新执行程序
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    # 2，执行自动化测试用例
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    # 3，进行文件生成（index.html好屌的样子哦）
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


def make_shell_context():
    """make_shell_context:
        shell使用方便（避免每次启动shell都需要
        创建或者导入DB）
    """
    # 利用字典，python的自省
    return dict(app=app, db=db,
                User=User, Role=Role, Post=Post)

# shell 命令
manager.add_command("shell", Shell(make_context=make_shell_context))
# 创建迁移数据库的shell命令
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()
