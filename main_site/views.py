# coding=utf-8
from flask import Response
from extensions import getGet

from main_site.collector_router import ApiRouter


def acollection(request):
    mode = getGet(request, "mode")
    router = ApiRouter(mode, request)
    resp, mime = router.execute()
    return Response(response=resp, mimetype=mime)