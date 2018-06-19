import json
import os

import sys
from flask import Flask, request, render_template, jsonify, Response, stream_with_context
from sqlalchemy import create_engine, Column, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.types import BIGINT, String

from main_site.views import acollection
from bots.views import index as bots_index
from models import *

app = Flask(__name__)
app.static_url_path = "/static"

engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
metadata = MetaData()
users_table = Table('users', metadata,
    Column('id', BIGINT, primary_key=True),
    Column('chat_id', BIGINT),
    Column('fname', String),
    Column('rank', String),
)
chats_table = Table('chats', metadata,
    Column('id', BIGINT, primary_key=True),
    Column('chat_name', String),
    Column('users_list', String),
)
metadata.create_all(engine)
mapper(ChatUser, users_table)
mapper(Chat, chats_table)
db_session = sessionmaker(bind=engine)


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


@app.route("/conversations_bot", methods=['GET', 'POST'])
def conversations_bot_route():
    #return Response(stream_with_context(bots_index(request)))
    return Response("ok")


@app.route("/nozomigrabber/<tag>/<int:maxpage>")
def test_route(tag, maxpage):
    from acollection.nozomilib.api import NozomiApi
    return Response(stream_with_context(NozomiApi().main(tag=tag, maxpage=maxpage)), mimetype="text/plain")


@app.route("/schd/")
def schd_route():
    return Response("ok", mimetype="text/plain")


if __name__ == '__main__':
    app.run(debug=True)