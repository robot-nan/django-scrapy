# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from django.forms import model_to_dict
# from hw.models import *

#
class TudouUserPipeline(object):
    def process_item(self, item, spider):
        try:
            item_model = item_to_model(item)
        except TypeError:
            return item
        try:
            tmp_item = dict(item)
            item_model.objects.create(**tmp_item)
        except Exception, e:
            print '1####################'
            print e
        print '1####################'
        return item
def item_to_model(item):
    """scrapy item  to django model"""
    model_class = getattr(item, 'django_model')
    if not model_class:
        raise TypeError("Item is not a `DjangoItem` or is misconfigured")
    return type(item.instance)
