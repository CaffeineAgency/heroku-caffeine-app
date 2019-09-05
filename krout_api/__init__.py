import json
import time
import os
import psycopg2
from flask import Response, request


def make_routes(app,):
    app.add_url_rule("/krout_api/<x>,<y>,<r>", "krout_list", krout_list)
    app.add_url_rule("/krout_api/route/add", "krout_add", krout_add, methods=["POST"])
    app.add_url_rule("/krout_api/approve/<id>/<administrator_token>", "krout_approve", krout_approve)


def krout_list(x, y, r):
    selection = selectFromDB(x, y, r)
    resp = {
        "time": time.time(),
        "current_position": {
            "x": x,
            "y": y,
            "r": r
        }
    }
    resp.update(selection)
    return Response(json.dumps(resp), mimetype="application/json")


def krout_add():
    x, y, sender, title, description, image_link = (request.form.get(t) for t in "x y sender title description image_link".split())

    selection = insertIntoDB(title, description, image_link, sender, x, y)
    resp = {
        "time": time.time(),
        "current_position": {
            "x": x,
            "y": y
        }
    }
    resp.update(selection)
    return Response(json.dumps(resp), mimetype="application/json")


def krout_approve(id, administrator_token):
    resp = {
        "time": time.time(),
    }
    if administrator_token == os.environ.get("admin_token", ""):
        selection = approvePlace(id)
        resp.update(selection)
    else:
        resp["errored"] = True
        resp["error"] = "Wrong administartor token"
    return Response(json.dumps(resp), mimetype="application/json")


def selectFromDB(x, y, r):
    DATABASE_URL = os.environ['DATABASE_URL']
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    records = []
    response = {
        "errored": False,
        "records": records
    }
    command = """
    SELECT
        *
    FROM 
        Places
    WHERE
        position <@ circle '(({x}, {y}), {r})' and approved;
    """.format(x=x, y=y, r=r)
    try:
        cur = connection.cursor()
        cur.execute(command)
        response["records"] = cur.fetchall()
        cur.close()
        connection.commit()
    except (Exception, connection.DatabaseError) as error:
        print(error)
        response["errored"] = True
        response["error"] = str(error)
    finally:
        if connection is not None:
            connection.close()
        return response


def insertIntoDB(title, description, image_link, sender, x, y):
    DATABASE_URL = os.environ['DATABASE_URL']
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    response = {
        "errored": False
    }
    #TODO: YES -> NO
    command = """
    INSERT INTO 
        Places (title, description, image_link, sentby, position, approved)
    VALUES
        ('{}', '{}', '{}', '{}', POINT({},{}), {});
    """.format(title, description, image_link, sender, x, y, "true")
    try:
        cur = connection.cursor()
        cur.execute(command)
        response["message"] = "ok"
        cur.close()
        connection.commit()
    except (Exception, connection.DatabaseError) as error:
        print(error)
        response["errored"] = True
        response["error"] = str(error)
    finally:
        if connection is not None:
            connection.close()
        return response


def approvePlace(id):
    DATABASE_URL = os.environ['DATABASE_URL']
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    response = {
        "errored": False
    }
    command = """
    UPDATE 
        Places
    SET
        (approved) = (yes);
    WHERE
        id = {}
    """.format(id)
    try:
        cur = connection.cursor()
        cur.execute(command)
        response["message"] = "ok"
        cur.close()
        connection.commit()
    except (Exception, connection.DatabaseError) as error:
        print(error)
        response["errored"] = True
        response["error"] = str(error)
    finally:
        if connection is not None:
            connection.close()
        return response
