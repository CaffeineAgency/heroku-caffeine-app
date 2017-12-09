# coding=utf-8
import jsonpickle
import os
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from acollection.useringroup.lib import VKGroupWorker

commands_list = ["help", "wake", "cmds", "check-subs", "check-like"]
groupsec = os.environ["rkkk_token"]

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
            try:
                recognized, parsed_command = try_parse_command(text.replace("~/", "").strip())
                if not recognized:
                    send_message(sender, "Ты бы мне ещё консервных банок насобирал!")
                    return HttpResponse("ok")
                send_message(sender, parsed_command)
            except Exception as e:
                send_message(307982226, e.args)
    elif type == "group_join":
        pass
    return HttpResponse("ok")


def execute_command(request):
    command, args = request
    if args is not None:
        args = args.split("|")
    if command == "help":
        return "**Тут (должен быть) краткий референс по использованию бота**\nАх да, аргументы надо отделять (\"|\")\nПример: ~/{command_name} arg1|arg2|3|(256)|..."
    elif command == "cmds":
        return "\n".join(commands_list)
    elif command == "wake":
        return "Awaken!"
    elif command == "check-subs":
        if args is None or len(args) < 2:
            return "Not enough arguments!\n~/check-subs UID|g1,g3,g4,g5"
        vgw = VKGroupWorker(groupsec)
        return vgw.isUserSubscribed(args[1], args[0])
    elif command == "check-like":
        if args is None or len(args) < 2:
            return "Not enough arguments!\n~/check-like UID|post_link"
        vgw = VKGroupWorker(groupsec, True)
        return vgw.isUserLikedPost(args[1], args[0])


def try_parse_command(text):
    command_parts = text.split()
    if command_parts[0] not in commands_list:
        return False, None
    if len(command_parts) == 2:
        request = command_parts[0], command_parts[1]
    else:
        request = command_parts[0], None
    return True, execute_command(request)

def send_message(uid, text):
    vkapi_endpoint = f"https://api.vk.com/method/messages.send?message={text}&user_id={uid}&access_token={groupsec}&v=5.69"
    requests.request("GET", vkapi_endpoint)
