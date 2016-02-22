from django.conf.urls import patterns, url

from instamap import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^getUserId/$', views.getUserId, name='getUserId')
)