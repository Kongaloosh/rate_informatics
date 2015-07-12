from django.conf.urls import patterns, include, url
from rate.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index, name='home'),
    url(r'^about$', about, name='about'),
    # Examples:
    # url(r'^$', 'rateinformatics.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
