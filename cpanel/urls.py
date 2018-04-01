from django.conf.urls import url

from cpanel import views

urlpatterns = (
    url(r'^cpanel', views.index, name='controlpanel'),
    url(r'^cpanel/register/$', views.RegisterFormView.as_view()),
    url(r'^cpanel/login/$', views.LoginFormView().as_view()),
    url(r'^cpanel/logout/$', views.LoginFormView().as_view()),
)
