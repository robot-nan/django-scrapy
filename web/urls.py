# coding:utf-8
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('web.views',
                       url(r'^gold/advice/now/$', 'gold_advice', name='gold advice'),
                       url(r'^kxt/(?P<date>.*)/$', 'get_kxt', name='get kxt'),
                       url(r'^get_investing/$', 'get_investing', name='get investing'),
                       url(r'^wezone/(?P<code>.*)/$', 'wezone', name='wezone'),
                       url(r'^stock_finance_sina/(?P<code>.*)/$', 'stock_finance_sina', name='stock finance sina'),
                       url(r'^caiku/(?P<code>.*)/$', 'caiku', name='caiku'),

                       url(r'^index/$', TemplateView.as_view(template_name='xinqihang/index.html'), name='caiku'),
                       url(r'^niuren/$', TemplateView.as_view(template_name='xinqihang/niuren.html'), name='caiku'),
                       url(r'^shuju/$', TemplateView.as_view(template_name='xinqihang/shuju.html'), name='caiku'),
                       url(r'^zhibo/$', TemplateView.as_view(template_name='xinqihang/zhibo.html'), name='caiku'),
                       )
