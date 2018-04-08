import os

from flask import Flask, request, render_template, Response

from main_site.views import acollection
from bots.views import index as bots_index

app = Flask(__name__, static_url_path="/static")

@app.route("/")
def main_route():
    return render_template("index.html")


@app.route("/acollection", methods=['GET'])
def acollection_route():
    return acollection(request)


@app.route("/bot")
def bot_route():
    return bots_index(request)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)