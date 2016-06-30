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
    composite_advice = models.CharField(u'综合建议', max_length=32, null=True, blank=True, unique=True)
    average_advice = models.CharField(u'平均指数建议', max_length=32, null=True, blank=True, unique=True)
    average_buy = models.CharField(u'平均购买', max_length=32, null=True, blank=True, unique=True)
    average_sell = models.CharField(u'平均出售', max_length=32, null=True, blank=True, unique=True)
    technology_advice = models.CharField(u'技术指标建议', max_length=32, null=True, blank=True, unique=True)
    technology_buy = models.CharField(u'技术指标购买', max_length=32, null=True, blank=True, unique=True)
    technology_sell = models.CharField(u'技术指标出售', max_length=32, null=True, blank=True, unique=True)
    show_data = models.CharField(u'更新区间', max_length=2, choices=GlOD_SHOW_TIME_CHOICE, default=u'0')


class GoldPivotPoint(BaseTime):
    """枢轴点"""
    name = models.ForeignKey('GoldName', related_name='gold_pivot_point')
    support1 = models.CharField(u'支撑位1', max_length=32, null=True, blank=True, unique=True)
    support2 = models.CharField(u'支撑位2', max_length=32, null=True, blank=True, unique=True)
    support3 = models.CharField(u'支撑位3', max_length=32, null=True, blank=True, unique=True)
    Pivot = models.CharField(u'轴点', max_length=32, null=True, blank=True, unique=True)
    drag1 = models.CharField(u'阻力位1', max_length=32, null=True, blank=True, unique=True)
    drag2 = models.CharField(u'阻力位2', max_length=32, null=True, blank=True, unique=True)
    drag3 = models.CharField(u'阻力位3', max_length=32, null=True, blank=True, unique=True)
    show_data = models.CharField(u'更新区间', max_length=2, choices=GlOD_SHOW_TIME_CHOICE, default=u'0')


class GoldName(models.Model):
    """枢轴点 名称"""
    name = models.CharField(u'名称', max_length=32, null=True, blank=True, unique=True)


class GoldTechniqueData(BaseTime):
    """技术指标"""
    symbol = models.ForeignKey('GoldName', related_name='gold_technique_data')
    get_time = models.CharField(u'官方更新时间', max_length=32, null=True, blank=True, unique=True)
    price = models.CharField(u'价值', max_length=32, null=True, blank=True, unique=True)
    oprate = models.CharField(u'操作', max_length=32, null=True, blank=True, unique=True)
    show_data = models.CharField(u'更新区间', max_length=2, choices=GlOD_SHOW_TIME_CHOICE, default=u'0')


class GoldSymbolName(models.Model):
    """技术指标 符号名 名字会变 如果没有要的名字就要重新写入进去"""
    name = models.CharField(u'符号名称', max_length=32, null=True, blank=True, unique=True)


class GoldMoveAverage(BaseTime):
    """移动平均指数"""
    get_time = models.CharField(u'官方更新时间', max_length=32, null=True, blank=True, unique=True)
    date_name = models.ForeignKey('GoldMoveDateName', related_name='gold_move_average')
    standard = models.CharField(u'标准', max_length=32, null=True, blank=True, unique=True)
    move = models.CharField(u'移动', max_length=32, null=True, blank=True, unique=True)
    show_data = models.CharField(u'更新区间', max_length=2, choices=GlOD_SHOW_TIME_CHOICE, default=u'0')


class GoldMoveDateName(models.Model):
    """移动平均指数 日期名字"""
    name = models.CharField(u'符号名称', max_length=32, null=True, blank=True, unique=True)
