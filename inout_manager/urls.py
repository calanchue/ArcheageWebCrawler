from django.conf.urls import patterns, url
from inout_manager import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^view$', views.view, name='view'),
)

