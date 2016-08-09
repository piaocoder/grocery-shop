# coding:utf8
from datetime import datetime
from flask import (render_template, session,
                   redirect, url_for, request,
                   current_app, flash,
                   make_response, abort)
from flask_login import (login_required, current_user)

from . import main
from .forms import (NameForm, EditProfileForm,
                    EditProfileAdminForm)
from .. import db
from ..email import send_mail
from ..models import (Role, User)
from ..decorators import admin_required


# @main.route('/', methods=['GET', 'POST'])
# def index():
#     user_agent = request.headers.get('User-Agent')
#     name = None
#     form = NameForm()
#     if form.validate_on_submit():
#         # 获取前一个输入的名称
#         oldName = session.get('name')
#
#         # 数据库操作
#         name = form.name.data
#         user = User.query.filter_by(username=name).first()
#         if user is None:
#             user = User(username=name)
#             db.session.add(user)
#             session['known'] = False
#             if current_app.config['MAIL_ADMIN']:
#                 send_mail(
#                     current_app.config['MAIL_ADMIN'],
#                     "New user", "mail/new_user",
#                     user=user)
#         else:
#             session['known'] = True
#
#         # 存储前一个输入的名称
#         session['name'] = name
#         if oldName and oldName != name:
#             flash("Looks like you have changed your name.")
#
#         # 蓝本中的不同地方
#         return redirect(url_for('.index'))
#     return render_template(
#         'index.html', user_agent=user_agent,
#         form=form, name=session.get('name'),
#         known=session.get('known', False)
#     )
@main.route('/')
def index():
    print '>>>>>>>>>>>>>>>>>>>>>>>>>>'
    print current_user.username
    print current_user.email
    print current_user.role
    print '>>>>>>>>>>>>>>>>>>>>>>>>>>'
    return render_template('index.html')


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.aboutMe = form.aboutMe.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.aboutMe.data = current_user.aboutMe
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    """edit_profile_admin
        admin_required: 为自定义修饰器相关函数

    :param id:
    """
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.aboutMe = form.aboutMe.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.aboutMe.data = user.aboutMe
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/cookie/<name>/')
def cookie(name):
    response = make_response(
        "<h1>Hello {}, "
        "we carry a cookie!</h1>".format(name))
    response.set_cookie('answer-bamboo', '100000')
    return response


@main.route('/index.html')
def index_ref():
    return render_template('index.html')


@main.route('/user/<username>/')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/redirect/')
def redirect_google():
    return redirect('http://www.google.com')
