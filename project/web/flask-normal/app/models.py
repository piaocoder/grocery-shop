# coding:utf8
"""
    请确保数据库已经存在哦
"""
from datetime import datetime
from werkzeug.security import (
    generate_password_hash, check_password_hash)
from itsdangerous import \
    TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import (UserMixin, AnonymousUserMixin)

from . import (db, loginManager)


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


# DB class (ORM)
class Role(db.Model):
    """角色"""
    # 表名
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # 默认角色和权限
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    # 表明该表被某一个指定的表当为外键映射
    users = db.relationship('User', backref='role', lazy='dynamic')


    @staticmethod
    def insert_roles():
        roles = {
            # 普通用户权限，默认角色
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        # 更新所有角色的权限信息
        for (r, value) in roles.items():
            role = Role.query.filter_by(name=r).first()
            if role is None:
                # 新增用户角色，DB中不存在
                role = Role(name=r)
            # 更新其他列的值
            role.permissions = value[0]
            role.default = value[1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return "<Role {}>".format(self.name)


class User(UserMixin, db.Model):
    """用户名,UserMixin保证可以使用current_user访问"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # passwd hash
    passwordHash = db.Column(db.String(128))
    # 邮件确认标志列
    confirmed = db.Column(db.Boolean, default=False)
    # 名字
    name = db.Column(db.String(64))
    # 所在地
    location = db.Column(db.String(64))
    # 关于我
    aboutMe = db.Column(db.Text())
    # 注册时间和上次访问时间
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, **kwargs):
        """__init__：初始化的同时对当前用户进行角色的赋予

        :param **kwargs:
        """
        super(User, self).__init__(**kwargs)
        if self.role is None:
            print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            print current_app.config['MAIL_ADMIN']
            print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            if self.email == current_app.config['MAIL_ADMIN']:
                self.role = Role.query.filter_by(
                    permissions=0xff).first()
                print '*************************'
                print 'Admonistration account'
                print self.role
                print '*************************'

            if self.role is None:
                self.role = Role.query.filter_by(
                    default=True).first()

    @property
    def password(self):
        """password：
            属性读取设定，不允许读取password，已经不存在或者加密
            password是一个虚构的存在，蛮有意思的。
        """
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        """password：赋值设定

        :param password:
        """
        self.passwordHash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.passwordHash, password)

    def generate_confirmation_token(self, expiration=3600):
        """generate_confirmation_token：生成token

        :param expiration:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        """confirm：确认token是否合法

        :param token:
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        """generate_reset_token：重置token信息

        :param expiration:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        """reset_password：重置密码

        :param token:
        :param new_password:
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        """generate_email_change_token：更改email并生成新的token

        :param new_email:
        :param expiration:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        """change_email：更改email

        :param token:
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def can(self, permissions):
        """can：权限检查

        :param permissions:
        """
        print '**************can****************'
        print self.role
        print '*********************************'
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        """is_administrator：是否为管理员"""
        return self.can(Permission.ADMINISTER)

    def ping(self):
        """ping：刷新上次访问时间"""
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def __repr__(self):
        return "<User {}>".format(self.username)


class AnonymousUser(AnonymousUserMixin):
    """AnonymousUser：匿名用户"""
    # 之后可以使用current_user.can()调用，内置
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False
loginManager.anonymous_user = AnonymousUser


@loginManager.user_loader
def load_user(userId):
    """load_user：加载用户的回调函数，找到用户，返回对象

    :param userId:
    """
    return User.query.get(int(userId))
