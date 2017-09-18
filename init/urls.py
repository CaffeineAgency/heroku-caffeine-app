from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^test', hello.views.test, name='test'),
    url(r'^admin/', include(admin.site.urls)),
]
