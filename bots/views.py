# coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import TemplateDoesNotExist

from init.extensions import getGet
import jsonpickle

def index(request):
    print(request)
    print(request.POST)
    return HttpResponse("HELLO!")
