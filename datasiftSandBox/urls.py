from django.conf.urls import patterns, url

from datasiftSandBox import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^createStream', views.createStream, name='createStream'),
    url(r'^getStreams', views.getStreams, name='getStreams'),
    url(r'^stopStream', views.stopStream, name='stopStream')

)