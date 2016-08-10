#!/usr/bin/env python
# coding:utf8
import os
from app import create_app, db
from app.models import (Role, User, Post)
from flask_script import (Manager, Shell)
from flask_migrate import (Migrate, MigrateCommand)


app = create_app(os.getenv("FLASK_CONFIG") or "default")
manager = Manager(app)
migrate = Migrate(app, db)


@manager.command
def test():
    """test:Run the unit test
        shell command：
            python manager.py test
    """
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


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
