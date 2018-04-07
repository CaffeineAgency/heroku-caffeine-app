from django.conf.urls import url
from django.contrib import admin

import bots.views
import hello.views

app_name="nuark-caffeine"

admin.autodiscover()

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^acollection', hello.views.acollection, name='apicol'),
    url(r'^bot', bots.views.index, name='botcol'),
]
