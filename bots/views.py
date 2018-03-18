# coding=utf-8
import jsonpickle
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from bots.BotController import BotController
from bots.GroupApiHooks import GroupApiHooks


@csrf_exempt
def index(request):
    inc_data = jsonpickle.decode(request.body)
    type = inc_data["type"]
    if type == "confirmation":
        if inc_data["group_id"] == 140299531:
            return HttpResponse("401176a7")
    elif type == "message_new":
        obj = inc_data["object"]
        hooker = GroupApiHooks()
        controller = BotController(obj, hooker)
        controller.execute()
    elif type == "group_join":
        obj = inc_data["object"]
        user_id, join_type = obj["user_id"], obj["join_type"]
        text = "Group join: \n" + GroupApiHooks().users_get(user_id)
        GroupApiHooks.notify_creator(text)
    return HttpResponse("ok")
