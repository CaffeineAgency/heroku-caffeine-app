import os

import sys
from flask import Flask, request, render_template, jsonify, Response
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


@app.route("/bot")
@app.route("/bot/")
def bot_route():
    return bots_index(request)


@app.route("/test")
def test_route():
    stream = Response().stream
    stream.write("t1")
    stream.write("t1")
    stream.write("t1")
    stream.write("t1")
    stream.write("t1")
    stream.close()


if __name__ == '__main__':
    if "create_db" in sys.argv:
        print("generating db...")
        db.create_all()
        print("success!")
    else:
        app.run(debug=True)