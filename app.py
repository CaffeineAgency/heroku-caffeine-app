import os

import sys
from flask import Flask, request, render_template, jsonify, Response, stream_with_context
from flask_sqlalchemy import SQLAlchemy

from main_site.views import acollection
from bots.views import index as bots_index

app = Flask(__name__)
app.static_url_path = "/static"
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)


@app.route("/")
def main_route():
    return render_template("index.html")


@app.route("/acollection", methods=['GET'])
def acollection_route():
    return acollection(request)


@app.route("/bot", methods=['GET', 'POST'])
@app.route("/bot/", methods=['GET', 'POST'])
def bot_route():
    return Response(stream_with_context(bots_index(request)))


@app.route("/test/<str:tag>/<int:maxpage>")
def test_route(tag, maxpage):
    from acollection.nozomilib.api import NozomiApi
    return Response(stream_with_context(NozomiApi().main(tag=tag, maxpage=maxpage)), mimetype="text/plain")

if __name__ == '__main__':
    if "create_db" in sys.argv:
        print("generating db...")
        db.create_all()
        print("success!")
    else:
        app.run(debug=True)