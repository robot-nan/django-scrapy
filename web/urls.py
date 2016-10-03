# coding:utf-8
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('web.views',
                       url(r'^gold/advice/now/$', 'gold_advice', name='gold advice'),
                       url(r'^kxt/(?P<date>.*)/$', 'get_kxt', name='get kxt'),
                       url(r'^get_investing/$', 'get_investing', name='get investing'),
                       url(r'^wezone/(?P<code>.*)/$', 'wezone', name='wezone'),
                       url(r'^k_line/stock/$', TemplateView.as_view(template_name='k_line.html'), name='k line stock'),
                       url(r'^k_line/get_data/(?P<code>.*)/$', 'get_k_line_data', name='get data'),
                       )
