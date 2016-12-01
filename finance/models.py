# coding:utf-8
from web.models import BaseTime
from django.db import models


class DayBuyPoint(BaseTime):
    point = models.IntegerField(u'买点', default=0)

    def __unicode__(self):
        return self.point


class StockPoint(BaseTime):
    date = models.CharField(u'日期', max_length=16)
    code = models.CharField(u'股票代码', max_length=16)
    price = models.CharField(u'价格', max_length=16)
    time = models.CharField(u'时间', max_length=32)
    type = models.CharField(u'类型', max_length=4)

    def __unicode__(self):
        return self.code

