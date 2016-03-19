#coding:utf8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
# 默认生成的表名 = APP + CLASS，例如books_publisher
class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    def __unicode__(self):
        """__unicode__:个性化显示"""
        return u'Name:{0}'.format(self.name)

class Author(models.Model):
    # 设置默认值
    first_name = models.CharField(
        max_length=30, default='bamboo', verbose_name='名')
    last_name = models.CharField(max_length=40, verbose_name='性')
    age = models.IntegerField(default=10)
    # 可以为空，非必选项
    # 添加标签名称
    email = models.EmailField(blank=True, verbose_name='e-mail')

    def __unicode__(self):
        """__unicode__"""
        return u'{0} {1}'.format(self.first_name, self.last_name)

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    # 设置日期、数字型为空
    publication_date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        """__unicode__"""
        return self.title
