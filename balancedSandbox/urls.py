from django.conf.urls import patterns, url

from balancedSandbox import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^stripe/$', views.stripe, name='stripe'),
    url(r'createCC', views.createCard),
)