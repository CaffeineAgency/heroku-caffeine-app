import json

import lxml.html
import requests
from flask import Response


def make_route(app):
    app.add_url_rule("/coub/<coub_id>", "coub_route", coub_route)


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