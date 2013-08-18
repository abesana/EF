from django.conf import settings
from django.conf.urls import patterns, url

import views

_url = '(?P<network>' + settings.NETWORKS + ')/username/(?P<username>\w+)/$'


urlpatterns = patterns('',
    url(_url, views.Profile.as_view())
)
