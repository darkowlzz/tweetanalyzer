from django.conf.urls.defaults import patterns, include, url
from tweetanalyzer.views import register
from tweetanalyzer.bmtu.views import tweet_list, follow, thanks, home
from django.contrib.auth.views import login, logout
from django.conf import settings
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', direct_to_template, {"template": "main.html",}),
    (r'^twitter/', include('twython_django_oauth.urls')),
    (r'^home/$', home),
    (r'^tweets/(?P<handler>\w+)/(?P<page>\d+)/$', tweet_list),
    (r'^tweets/(?P<handler>\w+)/$', tweet_list),
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout),
    (r'^accounts/register/$', register),
    (r'^follow/thanks/$', thanks),
    (r'^follow/form/$', follow),
    # Examples:
    # url(r'^$', 'mytwitter.views.home', name='home'),
    # url(r'^mytwitter/', include('mytwitter.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
