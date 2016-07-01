from django.conf.urls import patterns, include, url

urlpatterns = patterns('web.views',
                       url(r'^get/advice/now/$', 'glod_advice', name='glod advice'),
                       )