# coding:utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('finance.views',
                       url(r'^k_line/stock/(?P<code>.*)/$', 'get_k_day_data', name='k line stock'),

                       )
