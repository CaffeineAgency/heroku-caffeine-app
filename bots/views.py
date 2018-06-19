# coding=utf-8
import jsonpickle
from flask import stream_with_context

from extensions import getData

from bots.ConversationBotController import ConversationBotController
from bots.GroupApiHooks import GroupApiHooks


@stream_with_context
def bot_index(request):
    _json = getData(request)
    if _json:
        gids = {
            140299531: "rkkk_token",
            153656617: "cagency_token",
        }
        gid = gids.get(_json["group_id"])
        try:
            print("bot@Clyde > Ok, we got something:",_json)
            _type = _json["type"]
            if _type == "confirmation":
                cids = {
                    140299531: "401176a7",
                    153656617: "6bb6be65",
                }
                return cids.get(gid), "text/plain"
            else:
                yield "ok"
            if _type == "message_new":
                obj = _json["object"]
                if obj["body"].strip().startswith("."):
                    hooker = GroupApiHooks(gid=gid)
                    controller = BotController(obj, hooker)
                    controller.execute()
            elif _type == "group_join":
                obj = _json["object"]
                user_id, join_type = obj["user_id"], obj["join_type"]
                text = "Group join: " + GroupApiHooks(gid=gid).users_get(*[user_id]) + ", " + join_type
                GroupApiHooks(gid=gid).notify_creator(text, gid)
        except Exception as e:
            print(e, _json)
            GroupApiHooks(gid=gid).notify_creator("Error(s) happend: " + ", ".join(e.args), gid)
            raise e


def conversation_bot_index(request):
    yield "ok"
    _json = getData(request)
    print("bot@Celesta > Ok, we got something:", _json)
    if _json:
        try:
            if _json["type"] == "message_new":
                obj = _json["object"]
                text = obj["text"].strip().replace("[club153656617|@caffeincy] ", "")
                if text:
                    hooker = GroupApiHooks(gid="cagency_token")
                    controller = ConversationBotController(obj, hooker, text)
                    controller.execute()
        except Exception as e:
            GroupApiHooks(gid="cagency_token").notify_creator("Error(s) happend: " + ", ".join(e.args), "cagency_token")
            raise e
