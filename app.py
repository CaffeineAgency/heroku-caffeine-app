import os

from flask import Flask, request, render_template, Response, stream_with_context, session, redirect, send_file
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from vkmusic.views import render_response, vkm_logout
from vkmusic.views import do_auth
from extensions import getVal
import lxml.html
import requests
import json
import time

app = Flask(__name__)
app.secret_key = b'\xda\x9c\xd0\x9d\xcb\xac\xe9\x02@MQ\xbaFz\xad\xa2=\xb4Y\xaf\xd4k\xe9P'
app.static_url_path = "/static"
sockets = Sockets(app)


@app.route("/")
def main_route():
    return render_template("index.html")


@app.route("/coub/<coub_id>")
def coub_route(coub_id):
    r = requests.get("https://coub.com/view/{}".format(coub_id))
    if r.ok:
        d = lxml.html.fromstring(r.text)
        _json = json.loads(d.cssselect("script[type=text\/json]")[0].text.strip())
        _r = {
            "status": "ok",
            "title": _json["title"],
            "info": {
                "created": _json.get("created_at"),
                "update": _json["updated_at"],
                "published": _json["published_at"],
                "views": _json["views_count"],
                "thumb": _json["image_versions"]["template"].replace("%{version}", "big")
            },
            "music": {}
        }

        musicAuthor, musicTitle, download_link = [""]*3
        try: musicAuthor = d.cssselect(".musicAuthor")[0].text.strip()
        except: pass
        try: musicTitle = d.cssselect(".musicTitle")[0].text.strip()
        except: pass
        try: download_link = _json["file_versions"]["html5"]["audio"]["high"]["url"]
        except: pass

        _r["music"]["musicAuthor"] = musicAuthor
        _r["music"]["musicTitle"] = musicTitle
        _r["music"]["download_link"] = download_link

        resp = json.dumps(_r)
    else:
        resp = json.dumps({
            "status": "error",
            "msg": "This coub not exists or were hidden!"
        })
    return Response(resp, mimetype="application/javascript")


@app.route("/vkmusic/")
def vkmusic_route():
    return render_response(request, session)


@app.route("/vkmusic/vkm_auth", methods=['GET', 'POST'])
def vkmusic_auth_route():
    return do_auth(request, session)


@app.route("/vkmusic/vkm_logout", methods=['GET', 'POST'])
def vkmusic_deauth_route():
    return vkm_logout(request, session)


@app.route("/proxyfy", methods=['GET', 'POST'])
def proxyfy_route():
    l = getVal(request, "flink")
    m = getVal(request, "mime")
    if not (l and m):
        return "n-o-n-e"
    rs = requests.get(l)
    fn = "tmp/" + str(time.time()) + "." + l.split("?")[0].rsplit(".").pop()
    with open(fn, "wb+") as f:
        f.write(rs.content)
    return send_file(fn, mimetype=m)


@sockets.route("/echo")
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        ws.send(message)


def run(*args, **kwargs):
    print("Starting heroku-caffeine app...")
    port = int(os.environ.get("PORT", 80))
    print("Listening port:", port)
    server = pywsgi.WSGIServer(('0.0.0.0', port), app, handler_class=WebSocketHandler)
    print("Starting serve...")
    server.serve_forever()


if __name__ == "__main__":
    app.debug = True
    run()
