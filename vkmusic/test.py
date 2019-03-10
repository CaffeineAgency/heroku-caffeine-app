from flask import Response


def make_route(app):
    app.add_url_rule("/test", "t_route", test_route)


def test_route():
    return Response({"this": {"is": "success"}}, mimetype="application/javascript")