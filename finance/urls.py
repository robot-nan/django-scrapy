# coding:utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('finance.views',
                       url(r'^k_line/stock/(?P<code>.*)/$', 'get_k_day_data', name='k line stock'),
                       url(r'^stock/today_buy_point/(?P<code>.*)/$', 'today_buy_point', name='today buy point'),
                       url(r'^stock/stop_make_money/(?P<code>.*)/$', 'stop_make_money', name='stop make money'),
                       url(r'^stock/drag/(?P<code>.*)/$', 'drag', name='drag'),
                       url(r'^stock/tomorrow_buy_point/(?P<code>.*)/$', 'tomorrow_buy_point', name='tomorrow buy point'),
                       url(r'^stock/stop_loss/(?P<code>.*)/$', 'stop_loss', name='stop loss'),

                       )
