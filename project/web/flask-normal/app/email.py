from flask import current_app, render_template
from flask_mail import (Message)

from . import mail


def send_mail(to, subject, template, **kwargs):
    msg = Message(
        current_app.config['MAIL_SUBJECT'] + subject,
        sender=current_app.config['MAIL_SENDER'],
        recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
