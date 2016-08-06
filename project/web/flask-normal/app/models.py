# coding:utf8
"""
    请确保数据库已经存在哦
"""
from . import db


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
