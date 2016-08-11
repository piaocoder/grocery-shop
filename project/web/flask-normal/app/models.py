# coding:utf8
"""
    请确保数据库已经存在哦
"""
import hashlib
import bleach
from markdown import markdown
from datetime import datetime
from werkzeug.security import (
    generate_password_hash, check_password_hash)
from itsdangerous import \
    TimedJSONWebSignatureSerializer as Serializer
from flask import (current_app, request, url_for)
from flask_login import (UserMixin, AnonymousUserMixin)

from app.exceptions import ValidationError
from . import (db, loginManager)


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Post(db.Model):
    """Post：博客文章数据库表"""
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        userCount = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, userCount - 1)).first()
            p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                     timestamp=forgery_py.date.date(True),
                     author=u)
            db.session.add(p)
            db.session.commit()

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=self.id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author_id,
                              _external=True),
            'comments': url_for('api.get_post_comments', id=self.id,
                                _external=True),
            'comment_count': self.comments.count()
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            raise ValidationError('post does not have a body')
        return Post(body=body)


# 一旦文章更改，重新调用
db.event.listen(Post.body, 'set', Post.on_changed_body)


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


class Follow(db.Model):
    """Follow：关注与被关注关联表"""
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer,
                            db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer,
                            db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow)


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
    # 文章，每一个用户可以很多的文章
    avatar_hash = db.Column(db.String(32))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    # 当前用户关注了谁
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    # 谁关注了我
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     confirmed=True,
                     name=forgery_py.name.full_name(),
                     location=forgery_py.address.city(),
                     aboutMe=forgery_py.lorem_ipsum.sentence(),
                     member_since=forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @staticmethod
    def add_bifeng():
        u = User(email="bifeng@163.com",
                 username="bifeng",
                 password="mylove",
                 confirmed=True,
                 name="bifeng",
                 location="hazhou",
                 aboutMe="Wa",
                 member_since=datetime.now())
        db.session.add(u)
        db.session.commit()

    @staticmethod
    def add_self_follows():
        """add_self_follows:数据库的自我更新自动化脚本
                不用每次都手动的删除数据库
        """
        for user in User.query.all():
            if not user.is_following(user):
                user.follow(user)
                db.session.add(user)
                db.session.commit()

    def __init__(self, **kwargs):
        """__init__：初始化的同时对当前用户进行角色的赋予

        :param **kwargs:
        """
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['MAIL_ADMIN']:
                self.role = Role.query.filter_by(
                    permissions=0xff).first()

            if self.role is None:
                self.role = Role.query.filter_by(
                    default=True).first()
        # 关注自身
        self.follow(self)

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
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        """is_administrator：是否为管理员"""
        return self.can(Permission.ADMINISTER)

    def ping(self):
        """ping：刷新上次访问时间"""
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def is_following(self, user):
        """is_following：是否关注了user

        :param user:
        """
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    def follow(self, user):
        """follow：执行关联表的操作

        :param user:
        """
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f is not None:
            db.session.delete(f)

    def is_followed_by(self, user):
        """is_followed_by：是否被user关注了

        :param user:
        """
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    @property
    def followed_posts(self):
        return Post.query.join(
            Follow, Follow.followed_id == Post.author_id)\
            .filter(Follow.follower_id == self.id)

    def to_json(self):
        """to_json:有选择的返回json信息"""
        json_user = {
            'url': url_for('api.get_user', id=self.id, _external=True),
            'username': self.username,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'posts': url_for('api.get_user_posts', id=self.id, _external=True),
            'followed_posts': url_for('api.get_user_followed_posts',
                                      id=self.id, _external=True),
            'post_count': self.posts.count()
        }
        return json_user

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

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


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        json_comment = {
            'url': url_for('api.get_comment', id=self.id, _external=True),
            'post': url_for('api.get_post', id=self.post_id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author_id,
                              _external=True),
        }
        return json_comment

    @staticmethod
    def from_json(json_comment):
        body = json_comment.get('body')
        if body is None or body == '':
            raise ValidationError('comment does not have a body')
        return Comment(body=body)


db.event.listen(Comment.body, 'set', Comment.on_changed_body)
