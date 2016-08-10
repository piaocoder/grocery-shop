# coding:utf8
from flask_wtf import Form
from wtforms import (StringField, SubmitField,
                     TextAreaField, BooleanField,
                     SelectField)
from wtforms.validators import (
    Required, Length, Email, Regexp)
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField

from ..models import (Role, User)


class NameForm(Form):
    name = StringField("What is your name?",
                       validators=[Required()])
    submit = SubmitField("submit")


class EditProfileForm(Form):
    """EditProfileForm：普通用户资料编辑器"""
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    aboutMe = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(Form):
    """EditProfileAdminForm：管理员资料编辑器"""
    email = StringField('Email', validators=[
        Required(), Length(1, 64), Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, '
               'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    # 下拉列表
    role = SelectField('Role', coerce=int)
    # 普通信息
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    aboutMe = TextAreaField('About me')
    # 提交
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [
            (role.id, role.name)
            for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        """validate_email：校验新的邮箱

        :param field:
        """
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        """validate_username：校验用户名，这不是唯一的？我去

        :param field:
        """
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class PostForm(Form):
    """PostForm：博客文章表单"""
    # body = TextAreaField("What's on your mind?", validators=[Required()])
    body = PageDownField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')


class CommentForm(Form):
    body = StringField('Enter your comment', validators=[Required()])
    submit = SubmitField('Submit')
