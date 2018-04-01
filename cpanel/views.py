# coding=utf-8
from django.contrib.auth import login
from django.shortcuts import render_to_response
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import jsonpickle

def index(request):
    return render_to_response('cpanel.html')


class LoginFormView(FormView):
    form_class = AuthenticationForm
    success_url = "/cpanel/"
    template_name = "auth.html"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/cpanel/"
    template_name = "auth.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)
