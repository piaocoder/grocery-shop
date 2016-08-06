# coding:utf8
from flask import Blueprint

main = Blueprint('main', __name__)

# 错误处理和视图函数
from . import views, errors
