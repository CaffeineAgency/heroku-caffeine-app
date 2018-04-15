import json
import os

import sys
from flask import Flask, request, render_template, jsonify, Response, stream_with_context
from sqlalchemy import create_engine, Column, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.types import Integer, String, ARRAY as Array

from main_site.views import acollection
from bots.views import index as bots_index
from models import *

app = Flask(__name__)
app.static_url_path = "/static"

engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
metadata = MetaData()
users_table = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('chat_id', Integer),
    Column('fname', String),
    Column('rank', String),
)
chats_table = Table('chats', metadata,
    Column('id', Integer, primary_key=True),
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


@app.route("/nozomigrabber/<tag>/<int:maxpage>")
def test_route(tag, maxpage):
    from acollection.nozomilib.api import NozomiApi
    return Response(stream_with_context(NozomiApi().main(tag=tag, maxpage=maxpage)), mimetype="text/plain")


@app.route("/schd/")
def schd_route():
    return Response("ok", mimetype="text/plain")


@app.route("/db/<do>/")
def db_route(do):
    db = db_session()
    if do == "create":
        chat = Chat(88005553535, "Hmm1", json.dumps([8800, 5553, 535]))
        db.add(chat)
        chat = Chat(12345678976, "Hdd2",  json.dumps([71, 931]))
        print(chat)
        db.add(chat)
        db.commit()
        user = ChatUser(8800, 88005553535, "G P", 0)
        db.add(user)
        user = ChatUser(5553, 88005553535, "G D", 1)
        db.add(user)
        user = ChatUser(535, 12345678976, "T F", 2)
        db.add(user)
        user = ChatUser(71, 12345678976, "D V", 1)
        db.add(user)
        user = ChatUser(931, 12345678976, "S G", 2)
        db.add(user)
        db.commit()
        return "ZBS"
    elif do == "show":
        def enumer():
            for instance in db.query(ChatUser):
                yield repr(instance) + "\n"
        return Response(stream_with_context(enumer()), mimetype="text/plain")




if __name__ == '__main__':
    app.run(debug=True)