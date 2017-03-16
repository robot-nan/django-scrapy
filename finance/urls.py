# coding:utf-8
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('finance.views',
                       url(r'^k_line/(?P<code>.*)/$', 'ticks', name='ticks'),

                       url(r'^finance_k/(?P<code>.*)/$', 'finance_k', name='tradingview'),
                       url(r'^config/$', 'tradingview_config', name='tradingview_config'),
                       url(r'^symbols/$', 'symbol_info', name='symbol_info'),
                       url(r'^search/$', 'search', name='search'),

                       url(r'^history$', 'markets', name='market'),
                       url(r'^get_k_ticks_data/(?P<code>.*)/$', 'get_k_ticks_data', name='get k ticks data'),
                       url(r'^day_k_line/(?P<code>.*)/$', 'get_day_k_line', name='day k line'),


                       url(r'^set_point/chinayunju/112233/$', 'set_point', name='set point'),
                       url(r'^stock/today_buy_point/(?P<code>.*)/$', 'today_buy_point', name='today buy point'),
                       url(r'^stock/stop_make_money/(?P<code>.*)/$', 'stop_make_money', name='stop make money'),
                       url(r'^stock/drag/(?P<code>.*)/$', 'drag', name='drag'),
                       url(r'^stock/tomorrow_buy_point/(?P<code>.*)/$', 'tomorrow_buy_point', name='tomorrow buy point'),
                       url(r'^stock/stop_loss/(?P<code>.*)/$', 'stop_loss', name='stop loss'),


                       )

