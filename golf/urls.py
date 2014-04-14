from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', EmailIndex.as_view(), name='index'),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^accounts/', include('authtools.urls')),
    url(r'^tracker/', include('tracker.urls', namespace="tracker")),
)
