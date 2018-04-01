from django.conf.urls import include, url
from django.contrib import admin

import cpanel.views
import cpanel.urls
import hello.views
import bots.views

app_name="nuark-caffeine"

admin.autodiscover()

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^acollection', hello.views.acollection, name='apicol'),
    url(r'^bot', bots.views.index, name='botcol'),
    url(r'^admin/', admin.site.index, name='adminpanel'),
    *cpanel.urls.urlpatterns
]
