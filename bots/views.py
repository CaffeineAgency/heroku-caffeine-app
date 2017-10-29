# coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import TemplateDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from init.extensions import getGet
import jsonpickle

@csrf_exempt
def index(request):
    inc_data = jsonpickle.decode(request.body)
    type = inc_data["type"]
    if type == "confirmation":
        if inc_data["group_id"] == 140299531:
            return HttpResponse("401176a7")
    else:
        return HttpResponse("PASSED!")
