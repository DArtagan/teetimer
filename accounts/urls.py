from django.conf.urls import patterns, url, include

from accounts.views import *

urlpatterns = patterns('',
    # Companies
    url(r'^admin_users/$', Admins.as_view(), name='admin_users'),
    url(r'^admin_users/promote/(?P<pk>\d+)/$', promote, name='promote'),
    url(r'^admin_users/demote/(?P<pk>\d+)/$', demote, name='demote'),
    url(r'^add_user/$', AddUser.as_view(), name='add_user'),
    url(r'^update_email/$', EmailUpdate.as_view(), name='update_email'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    'authtools.views.password_reset_confirm_and_login',
    name='password_reset_confirm'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)
