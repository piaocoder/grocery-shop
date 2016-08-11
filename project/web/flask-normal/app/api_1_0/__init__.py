# coding:utf8
"""
    API程序子集
"""
from flask import Blueprint

api = Blueprint('api', __name__)

from . import authentication, posts, users, comments, errors
