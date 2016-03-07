#coding:utf8
from django.contrib import admin
from books.models import (
    Publisher, Author, Book)

# Register your models here.

# 将自定义的数据库models加入到admin管理界面中，以便
# 更好的操作
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Book)
