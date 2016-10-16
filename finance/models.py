# coding:utf-8
from web.models import BaseTime
from django.db import models


class DayBuyPoint(BaseTime):
    point = models.IntegerField(u'买点', default=0)

    def __unicode__(self):
        return self.point
