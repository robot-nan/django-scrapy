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


class GoldAdvice(BaseTime):
    """综合建议"""
    composite_advice = models.CharField(u'综合建议', max_length=32, null=True, blank=True)
    average_advice = models.CharField(u'平均指数建议', max_length=32, null=True, blank=True)
    average_buy = models.CharField(u'平均购买', max_length=32, null=True, blank=True)
    average_sell = models.CharField(u'平均出售', max_length=32, null=True, blank=True)
    technology_advice = models.CharField(u'技术指标建议', max_length=32, null=True, blank=True)
    technology_buy = models.CharField(u'技术指标购买', max_length=32, null=True, blank=True)
    technology_sell = models.CharField(u'技术指标出售', max_length=32, null=True, blank=True)
    show_data = models.CharField(u'更新区间', max_length=2, choices=GlOD_SHOW_TIME_CHOICE, default=u'0')
    show_team = models.DateTimeField(u'组')

