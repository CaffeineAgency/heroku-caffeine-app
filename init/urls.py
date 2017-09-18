from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import site.views

urlpatterns = [
    url(r'^$', site.views.index, name='index'),
    url(r'^test', site.views.test, name='test'),
    url(r'^admin/', include(admin.site.urls)),
]
