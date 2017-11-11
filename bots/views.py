# coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import TemplateDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from vk_api import vk_api

from init.extensions import getGet
import jsonpickle

commands_list = []
groupsec = "05f59078d7cfe924415b7f162a1e1eace16a9aaa30f969e51636808ce1d317cb7fc5957f7925c9364c258"

@csrf_exempt
def index(request):
    try:
        sess = vk_api.VkApi(app_id=6157263, api_version="5.69", token=groupsec, scope=266240)
        sess.auth()
        api = sess.get_api()
        inc_data = jsonpickle.decode(request.body)
        type = inc_data["type"]
        if type == "confirmation":
            if inc_data["group_id"] == 140299531:
                return HttpResponse("401176a7")
        elif type == "message_new":
            obj = inc_data["object"]
            sender = obj["user_id"]
            text = obj["body"]
            if text.startswith("~/"):
                api.message.send(user_id=sender, message="Wait for command recognition...")
                recognized, parsed_command = try_parse_command(text)
                if not recognized:
                    api.message.send(user_id=sender, message="Command not recognized")

        elif type == "group_join":
            pass
        else:
            return HttpResponse("ok")
    except vk_api.VkApiError as e:
        return HttpResponse(e.args)
    except:
        return HttpResponse("иди нахуй")
    return HttpResponse("ok")

def try_parse_command(text):
    command_parts = text.split()
    if command_parts[0] not in commands_list:
        return False, None
    return False, None
