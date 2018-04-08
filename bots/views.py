# coding=utf-8
import jsonpickle
from extensions import getData

from bots.BotController import BotController
from bots.GroupApiHooks import GroupApiHooks


def index(request):
    _json = getData(request)
    inc_data = jsonpickle.decode(_json)
    gids = {
        140299531: "rkkk_token",
        153656617: "cagency_token",
    }
    gid = gids.get(inc_data["group_id"])
    try:
        print("bot@Clyde > Ok, we got something:",inc_data)
        type = inc_data["type"]
        if type == "confirmation":
            cids = {
                140299531: "401176a7",
                153656617: "6bb6be65",
            }
            return cids.get(gid), "text/plain"
        elif type == "message_new":
            obj = inc_data["object"]
            if obj["body"].strip().startswith("."):
                hooker = GroupApiHooks(gid=gid)
                controller = BotController(obj, hooker)
                controller.execute()
        elif type == "group_join":
            obj = inc_data["object"]
            user_id, join_type = obj["user_id"], obj["join_type"]
            text = "Group join: " + GroupApiHooks(gid=gid).users_get(*[user_id]) + ", " + join_type
            GroupApiHooks(gid=gid).notify_creator(text, gid)
    except Exception as e:
        print(e, inc_data)
        GroupApiHooks(gid=gid).notify_creator("Error(s) happend: " + ", ".join(e.args), gid)
        raise e
    return "ok", "text/plain"
