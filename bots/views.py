# coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import TemplateDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from init.extensions import getGet
import jsonpickle

@csrf_exempt
def index(request):
    try:
        inc_data = jsonpickle.decode(request.body)
        type = inc_data["type"]
        if type == "confirmation":
            if inc_data["group_id"] == 140299531:
                return HttpResponse("401176a7")
        elif type == "message_new":
            pass
        elif type == "group_join":
            pass
        else:
            return HttpResponse("err")
    except:
        return HttpResponse("THIS PAGE FOR BOT! NOT FOR HUMANS!")
