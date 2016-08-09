# coding:utf8
from flask import Blueprint

main = Blueprint('main', __name__)

# 错误处理和视图函数
from . import views, errors
# 上下文处理器
from ..models import Permission


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
