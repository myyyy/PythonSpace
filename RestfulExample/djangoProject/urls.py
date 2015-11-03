# coding=utf-8
from django.conf.urls import include, url
from django.contrib import admin
from restful.views import teacher_list

urlpatterns = [
    # Examples:
    # url(r'^$', 'workPush.views.home', name='home'),
    url(r'^teacher/(\d+)', teacher_list),
    url(r'^admin/', include(admin.site.urls)),
]

