from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout_then_login
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from bbsApp.views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bbs.views.home', name='home'),
    # url(r'^bbs/', include('bbs.foo.urls')),
    url(r'^$',index),
    url(r'^about/$',about),
    url(r'^comment/$',comment),
    url(r'^edit/$',edit),
    url(r'^modify/$',modify),
    url(r'^findpassword/$',findpassword),
    url(r'^(\w+)/$',post_id),
    url(r'^(\w+)/edit/(\w+)/$',post_id_edit),
    url(r'^(\w+)/delete/(\w+)/$',post_id_delete),
    url(r'^accounts/login/$',  login),
    url(r'^accounts/logout/$', logout_then_login),
    url(r'^accounts/register/$', register),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()