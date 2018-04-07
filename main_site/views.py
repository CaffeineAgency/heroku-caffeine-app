# coding=utf-8
from flask import Response

from main_site.collector_router import ApiRouter
from init.extensions import getGet

def acollection(request):
    mode = getGet(request, "mode")
    router = ApiRouter(mode, request)
    resp, mime = router.execute()
    return Response(response=resp, mimetype=mime)