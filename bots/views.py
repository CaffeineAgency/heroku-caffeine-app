# coding=utf-8
import jsonpickle
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from bots.BotController import BotController
from bots.GroupApiHooks import GroupApiHooks


@csrf_exempt
def index(request):
    inc_data = jsonpickle.decode(request.body)
    cids = {
        140299531: "401176a7",
        153656617: "6bb6be65",
    }
    try:
        print("bot@Clyde > Ok, we got something: " + inc_data)
        type = inc_data["type"]
        if type == "confirmation":
            return HttpResponse(content=cids.get(inc_data["group_id"]))
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
    except Exception as e:
        print(inc_data)
        GroupApiHooks.notify_creator("Error(s) happend: " + ", ".join(e.args))
        raise e
    return HttpResponse(content="ok")
