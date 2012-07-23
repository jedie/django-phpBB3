from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

from sitemap import SitemapForum, SitemapTopic
from forms import RegistrationFormUtfUsername
from djangobb_forum import settings as forum_settings
from django.views.generic.simple import direct_to_template


admin.autodiscover()

sitemaps = {
    'forum': SitemapForum,
    'topic': SitemapTopic,
}

urlpatterns = patterns('',
    # Admin
    (r'^admin/', include(admin.site.urls)),

    # Sitemap
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    # Apps
    (r'^forum/account/', include('django_authopenid.urls')),
    (r'^forum/', include('djangobb_forum.urls', namespace='djangobb')),

    (r"^$", direct_to_template, {"template": "index.html"}),
)

# PM Extension
if (forum_settings.PM_SUPPORT):
    urlpatterns += patterns('',
        (r'^forum/pm/', include('django_messages.urls')),
   )

if (settings.DEBUG):
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'),
            'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
