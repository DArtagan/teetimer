from django.conf.urls import patterns, include, url

from golf.views import Index

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^accounts/', include('authtools.urls')),
    url(r'^textbits/', include('extra.urls', namespace='textbits')),
    url(r'^$', Index.as_view(), name='index'),
    url(r'^', include('tracker.urls', namespace='tracker')),
)
