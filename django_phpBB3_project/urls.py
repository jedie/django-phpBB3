from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.shortcuts import redirect

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_phpBB3.views.home', name='home'),
    # url(r'^django_phpBB3/', include('django_phpBB3.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # redirect root view to admin page:
    url(r'^$', lambda x:redirect("admin:index")),
)
