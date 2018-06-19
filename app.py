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
    def resp():
        yield "ok"
        cbot_index(request)
    return Response(resp())


@app.route("/nozomigrabber/<tag>/<int:maxpage>")
def test_route(tag, maxpage):
    from acollection.nozomilib.api import NozomiApi
    return Response(stream_with_context(NozomiApi().main(tag=tag, maxpage=maxpage)), mimetype="text/plain")


@app.route("/schd/")
def schd_route():
    return Response("ok", mimetype="text/plain")


if __name__ == '__main__':
    app.run(debug=True)