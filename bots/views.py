# coding=utf-8
import requests
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import TemplateDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from vk_api import vk_api

from init.extensions import getGet
import jsonpickle

commands_list = ["help", "clear"]
groupsec = "05f59078d7cfe924415b7f162a1e1eace16a9aaa30f969e51636808ce1d317cb7fc5957f7925c9364c258"

@csrf_exempt
def index(request):
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
            send_message(sender, "Wait for command recognition...")
            recognized, parsed_command = try_parse_command(text.replace("~/", "").strip())
            if not recognized:
                send_message(sender, "Command not recognized")
                return HttpResponse("ok")
            send_message(sender, parsed_command)
    elif type == "group_join":
        pass
    return HttpResponse("ok")

def try_parse_command(text):
    command_parts = text.split()
    if command_parts[0] not in commands_list:
        return False, None
    return False, command_parts[0]

def send_message(uid, text):
    vkapi_endpoint = f"https://api.vk.com/method/messages.send?message={text}&user_id={uid}&access_token={groupsec}&v=5.69"
    requests.request("GET", vkapi_endpoint)
