# coding=utf-8
from django.http import StreamingHttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import TemplateDoesNotExist

from init.extensions import getGet
import jsonpickle

from hello.worklogic import collect
from hello.worklogic.yandexdisk_worker import *
import acollection.ruminelib.api as rapi
import acollection.reactorlib.api as reapi

def index(request):
    try:
        return render_to_response('index.html')
    except TemplateDoesNotExist as ex:
        return HttpResponse(jsonpickle.encode(ex, unpicklable=False, max_depth=10))


def acollection(request):
    mode = getGet(request, "mode")
    if mode == "yagui":
        return render_to_response('yandexworker.html')
    if mode == "reactorgui":
        return render_to_response('reactorgallery.html')
    elif mode == "ubl":
        url = getGet(request, "u")
        filename = getGet(request, "f")
        id = upload_file_by_link(url, filename)
        return HttpResponse(id)
    elif mode == "ubf":
        url = getGet(request, "u")
        return HttpResponse(download_and_upload_file(url), content_type="text/plain")
    elif mode == "chk":
        id = getGet(request, "id")
        return HttpResponse(check_async_operation(id))
    elif mode == "col":
        collect.main()
    elif mode == "rumine":
        rq = dict()
        rq["threadId"] = getGet(request, "threadId")
        rq["pagenum"] = getGet(request, "pagenum")
        rq["b64"] = getGet(request, "b64")
        api = rapi.RuMineApi(request=rq)
        return HttpResponse(api.get_comments())
    elif mode == "reactorparser":
        rq = dict()
        rq["tag"] = getGet(request, "tag")
        rq["page"] = getGet(request, "page")
        api = reapi.ReactorApi()
        return HttpResponse(api.get_images(request=rq))
    elif mode == "download_image":
        url = getGet(request, "url")
        req = requests.get(url)
        return StreamingHttpResponse(req.raw, content_type=req.headers['content-type'])
    else:
        return HttpResponse("""
        СПРАВКА:
        // Все входные данные обязательны, если не указано обратное
        Существует три режима работы сервиса:
            'yagui' - GUI для yandexworker.
                Метод: GET
                Входные данные:
                    mode=yagui
            'rumine forum api' - парсит сообщения из форумных тредов сайта ru-minecraft.ru
                Метод: GET
                Входные данные:
                    mode=rumine
                    threadId=<threadId>
                    pagenum=<pagenum> - Не обязателен, если не указан, то берётся 9999999999999
                    b64=<any or y> - [WIP] Если "y", то конвертирует текст в base64(иногда бывает полезно).
            'reactor gallery' - Галерея пикч из джойреакторовского тега "красивые картинки".
                Метод: GET
                Входные данные:
                    mode=reactorgui
        """.encode("cp1251"), content_type="text/plain")



