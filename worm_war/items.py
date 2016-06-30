# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy_djangoitem import DjangoItem

from web.models import *
#
#
class GlodItem(DjangoItem):
    # fields for this item are automatically created from the django model
    django_model = GoldAdvice
    # v_category = Field()