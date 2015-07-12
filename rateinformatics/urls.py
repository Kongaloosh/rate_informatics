from django.conf.urls import patterns, include, url
from rate.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index, name='home'),
    url(r'^about$', about, name='about'),
    url(r'^c/add', add_a_course, name='add_a_course'),
    url(r'^l/add', add_a_lecturer, name='add_a_lecturer'),
    url(r'^r/add', add_a_response, name='add_a_response'),
    # Examples:
    # url(r'^$', 'rateinformatics.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
