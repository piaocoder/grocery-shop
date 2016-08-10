# coding:utf8
from flask import (current_app, render_template,
                   redirect, request, url_for, flash)
from flask_login import (login_user, logout_user,
                         login_required, current_user)

from . import auth
from .. import db
from ..models import User
from ..email import send_mail
from .forms import (LoginForm, RegistrationForm,
                    ChangePasswordForm,
                    PasswordResetRequestForm,
                    PasswordResetForm, ChangeEmailForm)


@auth.before_app_request
def before_request():
    """before_request：请求上下文钩子函数"""
    if current_user.is_authenticated:
        # 刷新上次访问时间
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """login：登陆函数，向base.html传入指定的变量
            用于判断是否登陆或者登出
        PS:最终会跳转到main主页的‘/’路由下
    """
    form = LoginForm()
    if form.validate_on_submit():
        # 邮箱
        user = User.query.filter_by(
            email=form.email.data).first()
        if user is not None and \
                user.verify_password(form.password.data):
            # 记录用户，cookie
            login_user(user, form.rememberMe.data)
            # 可能多个跳转，在这里有意义？用户等级？
            # next中记录原地址信息
            return redirect(request.args.get('next') or \
                            url_for('main.index'))
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # 写数据库操作
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        print '###########################'
        print user.role
        print '###########################'
        db.session.add(user)
        db.session.commit()
        # token，纯文本或者富文本在auth/email/confirm/目录下
        token = user.generate_confirmation_token()
        send_mail(user.email, "Confirm Your Account",
                  "auth/email/confirm", user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        # 跳转到login路由中
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    # current_user表示当前用户的数据库模型
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
    # 匿名用户那就不再关注？
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    """resend_confirmation：重新发送确认邮件"""
    token = current_user.generate_confirmation_token()
    send_mail(current_user.email, 'Confirm Your Account',
              'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))



@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template("auth/change_email.html", form=form)


@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('main.index'))
