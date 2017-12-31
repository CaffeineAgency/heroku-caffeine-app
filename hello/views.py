# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import TemplateDoesNotExist

from acollection.ydapi.yandexdisk_worker import *
from hello.collector_router import ApiRouter
from init.extensions import getGet


def index(request):
    try:
        return render_to_response('index.html')
    except TemplateDoesNotExist as ex:
        return HttpResponse(jsonpickle.encode(ex, unpicklable=False, max_depth=10))


def acollection(request):
    mode = getGet(request, "mode")
    router = ApiRouter(mode, request)
    return router.execute()