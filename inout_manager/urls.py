from django.conf.urls import patterns, url
from inout_manager import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^view$', views.view, name='view'),
    url(r'^bootstrap_test$', views.bootstrap_test, name='bootstrap_test'),
    url(r'^player$', views.recent_event, name='recent_event'),
    url(r'^player/(?P<player_name>.+)$', views.player_event, name='player_event'),
)

