from django.conf.urls import patterns, include, url

from extra.views import Update

urlpatterns = patterns('',
    url(r'^(?P<pk>.+)/update/$', Update.as_view(), name='update'),
)
