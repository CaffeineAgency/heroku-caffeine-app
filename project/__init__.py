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
    app.add_url_rule("/login", "vkmr_auth_login", _route_auth_login,  methods=['GET', 'POST'])
    app.add_url_rule("/logout", "vkmr_auth_logout", _route_auth_logout,  methods=['GET', 'POST'])
    app.add_url_rule("/vkmusic", "vkmr_main", _route_music,  methods=['GET', 'POST'])


def _route_auth_login():
    if "usert" in session:
        return redirect("/")
    login = getPost(request, "login")
    pwd = getPost(request, "pwd")
    data = {}
    if login and pwd:
        success, data = auth(login, pwd)
        if success:
            return redirect("/")
    return render_template(tpl_vm_auth, session=session, data=data)



def _route_auth_logout():
    deauth()
    return redirect("/")


def _route_music():
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


def deauth():
    session.pop("usert", None)
    session.modified = True
    return session


def auth(login, pwd):
    data = {}
    success = True
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
        session["udata"] = api.get_api().users_get()[0]
        session["usert"] = (api.login, api.token)
        session.modified = True
    return success, data
