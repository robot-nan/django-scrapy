# coding:utf-8
from __future__ import unicode_literals
from django.db import models

GlOD_SHOW_TIME_CHOICE = (

    (u'0', u'1分钟'),
    (u'1', u'5分钟'),
    (u'2', u'15分钟'),
    (u'3', u'30分钟'),
    (u'4', u'每小时'),
    (u'5', u'5小时'),
    (u'6', u'每日'),
    (u'7', u'每月'),
)


class BaseTime(models.Model):
    """基本模型，带创建更新时间"""
    created = models.DateTimeField(u'创建时间', auto_now_add=True)
    updated = models.DateTimeField(u'修改时间', auto_now=True)

    objects = models.Manager()

    class Meta:
        abstract = True
        ordering = ['-id', ]


class Yuncaijing(BaseTime):
    title = models.CharField(u'标题', max_length=256, null=True, blank=True)
    description = models.TextField(u'描述', blank=True, default=u'')
    content_info = models.TextField(u'文章内容', blank=True, default=u'')
    pub_time = models.CharField(u'发布时间', max_length=64, null=True, blank=True)

    def __unicode__(self):
        return self.title


class Guzhang(BaseTime):
    news_id = models.IntegerField(u'新闻ID', default=0)
    title = models.CharField(u'标题', max_length=256, null=True, blank=True)
    news_text = models.TextField(u'描述', blank=True, default=u'')
    news_time = models.CharField(u'发布时间', max_length=32, null=True, blank=True)
    real_time = models.CharField(u'发布时间', max_length=32, null=True, blank=True)
    news_time_title = models.CharField(u'发布时间', max_length=32, null=True, blank=True)
    class_name = models.CharField(u'发布时间', max_length=16, null=True, blank=True)
    news_all_text =  models.TextField(u'内容', blank=True, default=u'')

    def __unicode__(self):
        return self.title