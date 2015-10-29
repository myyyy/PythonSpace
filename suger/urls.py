#coding:utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from biger.views import RSSFeed
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'suger.views.home', name='home'),
    url(r'^biger/', include('biger.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','biger.views.home',name="home"),#主页
    url(r'^about/$','biger.views.about',name="about"),#关于我
    url(r'^message/$','biger.views.message',name="message"),#留言
    url(r'^archive/$','biger.views.archive',name="archive"),#归档
    url(r'^feed/$', RSSFeed(), name = "RSS"),  #新添加的urlconf, 并将name设置为RSS, 方便在模板中使用
    url(r'^search/$','biger.views.biger_search', name = "search"),#按文章标题搜索
    url(r'^biger/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<id>\d+)/$', 'biger.views.detail', name="detail"),#每篇文章 
    url(r'^biger/(?P<year>\d{4})/(?P<month>\d{1,2})/$','biger.views.archive_month',name="archive_month"),#按月归档
    url(r'^articleClassfi/(?P<classfi>\w+)/$', 'biger.views.classfiDetail', name="classfiDetail"),#每个分类页下面的文章
    url(r'^articleTag/(?P<tag>\w+)/$', 'biger.views.tagDetail', name="tagDetail"),#每个标签页下面的文章
)
