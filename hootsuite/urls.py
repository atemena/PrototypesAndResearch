from django.conf.urls import patterns, url

from hootsuite import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^shaSign/$', views.shaSign, name='shaSign')
)