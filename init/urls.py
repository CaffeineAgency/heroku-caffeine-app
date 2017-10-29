from django.conf.urls import include, url
from django.contrib import admin

import hello.views
import bots.views

admin.autodiscover()

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^acollection', hello.views.acollection, name='apicol'),
    url(r'^bot', bots.views.index, name='botcol'),
    url(r'^admin/', include(admin.site.urls)),
]
