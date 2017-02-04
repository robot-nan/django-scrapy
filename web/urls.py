# coding:utf-8
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('web.views',
                       url(r'^gold/advice/now/$', 'gold_advice', name='gold advice'),
                       url(r'^kxt/(?P<date>.*)/$', 'get_kxt', name='get kxt'),
                       url(r'^get_investing/(?P<code>.*)/$', 'get_investing', name='get investing'),
                       url(r'^wezone/(?P<code>.*)/$', 'wezone', name='wezone'),
                       url(r'^stock_finance_sina/(?P<code>.*)/$', 'stock_finance_sina', name='stock finance sina'),
                       url(r'^caiku/(?P<code>.*)/$', 'caiku', name='caiku'),
                       url(r'^jqka/(?P<code>.*)/$', 'jqka', name='jqka'),
                       url(r'^stock_price/(?P<code>.*)/$', 'stock_price', name='stock price'),
                       url(r'^stock_open_height_amount/(?P<code>.*)/$', 'stock_open_height_amount', name='stock open height amount'),
                       url(r'^stock_today_ditail/(?P<code>.*)/$', 'stock_today_ditail', name='stock today ditail'),

                       url(r'^index/$', TemplateView.as_view(template_name='xinqihang/index.html'), name='caiku'),
                       url(r'^niuren/$', TemplateView.as_view(template_name='xinqihang/niuren.html'), name='caiku'),
                       url(r'^shuju/$', TemplateView.as_view(template_name='xinqihang/shuju.html'), name='caiku'),
                       url(r'^zhibo/$', TemplateView.as_view(template_name='xinqihang/zhibo.html'), name='caiku'),
                       url(r'^about_us/$', TemplateView.as_view(template_name='xinqihang/about_us_shengming_jishu.html'), name='about us'),
                       url(r'^choose_stock/$', TemplateView.as_view(template_name='xinqihang/choose_stock.html'), name='choose stock'),
                       url(r'^diagnose/$', TemplateView.as_view(template_name='xinqihang/diagnose.html'), name='choose stock'),
                       url(r'^infomation/$', TemplateView.as_view(template_name='xinqihang/infomation.html'), name='infomation'),
                       url(r'^click/$', TemplateView.as_view(template_name='xinqihang/click.html'), name='click'),
                       url(r'^decision/$', TemplateView.as_view(template_name='xinqihang/decision.html'), name='decision'),
                       )


