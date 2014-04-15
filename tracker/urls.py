from django.conf.urls import patterns, include, url
from tracker.views import * 

urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', Detail.as_view(), name='detail'),
    url(r'^create/$', Create.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/update/$', Update.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', Delete.as_view(), name='delete'),
    url(r'^(?P<pk>\d+)/claim/$', claim, name="claim"),
    url(r'^(?P<date>[0-9]{4}-[0-9]{1,2}-[0-9]{1,2})/$', Date.as_view(), name='day'),
    url(r'^(?P<date>[0-9]{4}-[0-9]{1,2})/$', Month.as_view(), name='month'),
)
