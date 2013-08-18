from django.conf import settings
from django.conf.urls import patterns, url

import views

_base_url = '(?P<network>' + settings.NETWORKS + ')/username'
_url = _base_url + '/(?P<username>\w+)$'


urlpatterns = patterns('',
    url(_base_url + '$', views.ProfileMaker.as_view()),
    url(_url, views.Profile.as_view())
)
