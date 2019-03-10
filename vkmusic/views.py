# coding=utf-8
from flask import render_template, redirect
from vk_api import VkApi
from vkmusic.audio import VkAudio

from extensions import getPost

app_id = 5882810
v = "5.80"


def render_response(request, session):
    if "usert" in session and session["usert"]:
        log, tok = session["usert"]
        vapi = VkApi(login=log, token=tok)
        try:
            vapi.auth()
        except Exception as e:
            print(e.args)
            erdata = {
                "errored": True,
                "info": str(e.args)
            }
            return render_template("vkm_main.html", **erdata)
        else:
            vkaudio = VkAudio(vapi)
            tracks = vkaudio.get(0)
            data = {
                "usrhere": True,
                "tracks": tracks
            }
            return render_template("vkm_dashboard.html", **data)
    return render_template("vkm_main.html")


def do_auth(request, session):
    if request.method != "POST":
        return "-800 - U lose :D"
    login = getPost(request, "login")
    pwd = getPost(request, "pwd")
    if pwd and login:
        vapi = VkApi(login=login, password=pwd, app_id=app_id, api_version=v)
        try:
            vapi.auth()
        except Exception as e:
            print(e.args)
            erdata = {
                "errored": True,
                "info": str(e.args)
            }
            return render_template("vkm_main.html", **erdata)
        else:
            session["usert"] = (vapi.login, vapi.token)
            session.modified = True
            return render_response(request, session)
    return render_template("vkm_main.html", **{"errored": True})


def vkm_logout(request, session):
    session.pop("usert", None)
    session.modified = True
    return render_response(request, session)