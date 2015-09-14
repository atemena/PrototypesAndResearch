from django.conf.urls import patterns, url
from fbCanvas import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)