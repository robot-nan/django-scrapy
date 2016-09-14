# coding:utf-8
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('web.views',
                       url(r'^gold/advice/now/$', 'gold_advice', name='gold advice'),
                       url(r'^kxt/(?P<date>.*)/$', 'get_kxt', name='get kxt'),
                       url(r'^get_investing/$', 'get_investing', name='get investing'),
                       url(r'^wezone/(?P<code>.*)/$', 'wezone', name='wezone'),


                       url(r'^test1/$', TemplateView.as_view(template_name="play_data.html")),
                       url(r'^test2/$', TemplateView.as_view(template_name="pack.html")),
                       url(r'^test3/$', TemplateView.as_view(template_name="overview.html")),
                       url(r'^test4/$', TemplateView.as_view(template_name="inner.html")),
                       url(r'^test5/$', TemplateView.as_view(template_name="order.html")),
                       )
