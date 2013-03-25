from django.conf.urls import patterns, url
from inout_manager import views

urlpatterns = patterns('',
    url(r'^$', views.recent_event, name='index'),
    url(r'^view$', views.view, name='view'),
    url(r'^bootstrap_test$', views.bootstrap_test, name='bootstrap_test'),
    url(r'^player$', views.recent_event, name='recent_event'),
    url(r'^player/(?P<player_name>.+)$', views.player_event, name='player_event'),
    url(r'^expedition$', views.recent_exped_event, name='recent_exped_event'),
    url(r'^expedition/search_exped_event$', views.search_exped_event, name='search_exped_event'),
    url(r'^expedition/(?P<exped_name>.+)$', views.exped_event, name='exped_event'),
    url(r'^readme$', views.readme, name='readme'),
)

