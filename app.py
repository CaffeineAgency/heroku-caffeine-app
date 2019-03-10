import os

from flask import Flask, request, render_template, session, send_file
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

import coub_api
import vkmusic.test
from vkmusic.views import render_response, vkm_logout
from vkmusic.views import do_auth
from extensions import getVal
import requests
import time

app = Flask(__name__)
app.secret_key = b'\xda\x9c\xd0\x9d\xcb\xac\xe9\x02@MQ\xbaFz\xad\xa2=\xb4Y\xaf\xd4k\xe9P'
app.static_url_path = "/static"
sockets = Sockets(app)


@app.route("/")
def main_route():
    return render_template("index.html")

app = vkmusic.test.make_route(app)
app = coub_api.make_route(app)

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
    fn = "tmp/" + str(time.time())
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
