# coding: utf-8

from django.conf import settings
from django.conf.urls import patterns, include
from django.contrib import admin
from django.views.generic.simple import direct_to_template


admin.autodiscover()


urlpatterns = patterns('',
    # Admin
    (r'^admin/', include(admin.site.urls)),

    # Apps
    (r'^forum/', include('djangobb_forum.urls', namespace='djangobb')),

    (r"^$", direct_to_template, {"template": "index.html"}),
)

if (settings.DEBUG):
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'),
            'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
