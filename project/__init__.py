# coding=utf-8
from flask import render_template, redirect, request, session
from vk_api import VkApi
from project.audio import VkAudio

from extensions import *

app_id = 5882810
v = "5.80"

tpl_vm_auth = "vkm_auth.html"
tpl_vm_music = "vkm_music.html"


def make_routes(app):
    app.add_url_rule("/auth", "vkmr_auth", _route_auth,  methods=['GET', 'POST'])
    app.add_url_rule("/vkmusic", "vkmr_main", _route_music,  methods=['GET', 'POST'])


def _route_auth(request, session):
    is_user = "usert" in session
    action = getVal(request, "act")
    if action is not None:
        if is_user and action.lower() == "logout":
            if is_user:
                deauth(session)
        elif not is_user and action.lower() == "login":
            success, data, *_ = auth(request, session)
            if not success:
                render_template(tpl_vm_auth, session=session, data=data)
    return redirect("/")


def _route_music(request, session):
    is_user = "usert" in session
    try:
        if is_user:
            raise Exception("NO USER")
        login, token = session.get("usert")
        api = VkApi(login=login, token=token, app_id=app_id, api_version=v)
        api.auth()
    except:
        return redirect("/auth?act=login")
    music_api = VkAudio(api)
    data = {
        "tracks": music_api.get(0)
    }
    return render_template(tpl_vm_music, session=session, data=data)


def deauth(session):
    session.pop("usert", None)
    session.modified = True
    return session


def auth(request, session):
    data = {}
    success = True
    login = getPost(request, "login")
    pwd = getPost(request, "pwd")
    api = VkApi(login=login, password=pwd, app_id=app_id, api_version=v)
    try:
        api.auth()
    except Exception as e:
        data = {
            "witherror": True,
            "info": "; ".join(e.args)
        }
        success = False
    else:
        session["usert"] = (api.login, api.token)
        session.modified = True
    return success, data, request, session
