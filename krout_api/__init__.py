import json
import time
import lxml.html
import requests
from flask import Response

connection = None

def make_routes(app, conn):
    global connection
    connection = conn
    app.add_url_rule("/krout_api/<x>,<y>,<r>", "krout_list", krout_list)


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
    return Response(resp, mimetype="application/javascript")

def selectFromDB(x, y, r):
    global connection
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
        records = cur.fetchall()
        for i, row in enumerate(records):
            print(i, row)
        cur.close()
    except (Exception, connection.DatabaseError) as error:
        print(error)
        response["errored"] = True
        response["error"] = str(error)
    finally:
        if connection is not None:
            connection.close()
        return response
