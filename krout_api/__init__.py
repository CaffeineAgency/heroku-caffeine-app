import json
import time
import os
import psycopg2
from flask import Response

def make_routes(app,):
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
    return Response(json.dumps(resp), mimetype="application/javascript")

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
    except (Exception, connection.DatabaseError) as error:
        print(error)
        response["errored"] = True
        response["error"] = str(error)
    finally:
        if connection is not None:
            connection.close()
        return response
