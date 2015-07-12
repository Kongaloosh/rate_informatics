from django.conf.urls import patterns, include, url
from rate.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index, name='home'),
    url(r'^about$', about, name='about'),
    url(r'^courses/$', courses, name='course_list'),
    url(r'^c/add$', add_a_course, name='add_a_course'),
    url(r'^course/(?P<course_initials>.+)/', course, name='course'),
    url(r'^lecturers$', lecturers, name='lecturer_list'),
    url(r'^l/(?P<first_name>\w+)_(?P<last_name>\w+)', lecturer, name='lecturer'),
    url(r'^l/add', add_a_lecturer, name='add_a_lecturer'),
    url(r'^r/add', add_a_response, name='add_a_response'),
    url(r'^admin/', include(admin.site.urls)),
)
