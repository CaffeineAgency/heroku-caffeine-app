from flask import Flask, request, render_template, Response, stream_with_context

from bots.views import bot_index as bots_index, conversation_bot_index as cbot_index

app = Flask(__name__)
app.static_url_path = "/static"

@app.route("/")
def main_route():
    return render_template("index.html")


@app.route("/acollection", methods=['GET'])
def acollection_route():
    from main_site.views import acollection
    return acollection(request)


@app.route("/bot", methods=['GET', 'POST'])
@app.route("/bot/", methods=['GET', 'POST'])
def bot_route():
    return Response(bots_index(request))


@app.route("/conversations_bot", methods=['GET', 'POST'])
def conversations_bot_route():
    @stream_with_context
    def resp():
        yield "ok"
        cbot_index(request)
    return Response(resp())


@app.route("/nozomigrabber/<tag>/<int:maxpage>")
def test_route(tag, maxpage):
    from acollection.nozomilib.api import NozomiApi
    return Response(stream_with_context(NozomiApi().main(tag=tag, maxpage=maxpage)), mimetype="text/plain")


@app.route("/coub/<coub_id>")
def coub_route(coub_id):
    import requests, lxml.html, json
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


@app.route("/schd/")
def schd_route():
    return Response("ok", mimetype="text/plain")


if __name__ == '__main__':
    app.run(debug=True)