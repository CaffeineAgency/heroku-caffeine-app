from django.http import StreamingHttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import TemplateDoesNotExist

from init.extensions import getGet
import jsonpickle

from hello.worklogic import collect
from hello.worklogic.yandexdisk_worker import *
import hello.worklogic.ruminecraft_worker as RuMineApi

def index(request):
    try:
        return render_to_response('index.html')
    except TemplateDoesNotExist as ex:
        return HttpResponse(jsonpickle.encode(ex, unpicklable=False, max_depth=10))


def acollection(request):
    mode = getGet(request, "mode")
    if mode == "gui":
        try:
            return render_to_response('yandexworker.html')
        except TemplateDoesNotExist as ex:
            return HttpResponse(jsonpickle.encode(ex, unpicklable=False, max_depth=10))
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
        stat = jsonpickle.decode(api.check_async_operation(id)).get("status")
        return HttpResponse(stat)
    elif mode == "col":
        collect.main()
    elif mode == "stream":
        return StreamingHttpResponse([x for x in range(500000)])
    elif mode == "rumine":
        rq = dict()
        rq["threadId"] = getGet(request, "threadId")
        rq["pagenum"] = getGet(request, "pagenum")
        rq["b64"] = getGet(request, "b64")
        return HttpResponse(RuMineApi.get_comments(rq))
    else:
        return HttpResponse("""
        СПРАВКА:
		// Все методы обязательны, если не указано обратное
        Существует три режима работы сервиса:
            'uploading file by link'
                Метод: GET
                Входные данные:
                    mode=ubl
                    u=<url>
                    f=<filename> - можно не указывать
            'download and upload file' - Позволяет обойти ограничение яндекса на файлы, запрещённые на территории РФ. Не загружайте большие файлы.
                Метод: GET
                Входные данные:
                    mode=ubf
                    u=<url>
            'gui' - GUI для yandexworker.
                Метод: GET
                Входные данные:
                    mode=gui
            'async operation checker' - Проверяет статус асинхронной операции с диском яндекса.
                Метод: GET
                Входные данные:
                    mode=chk
                    id=<id>
            'collect.main' - Пока в разработке.
			'rumine forum api' - парсит сообщения из форумных тредов сайта ru-minecraft.ru
                Метод: GET
                Входные данные:
                    mode=rumine
                    threadId=<threadId>
                    pagenum=<pagenum> - Не обязателен, если не указан, то берётся 9999999999999
                    b64=<b64> - Не обязателен, если указан, то конвертирует текст в base64(иногда бывает полезно)
        """.encode("cp1251"), content_type="text/plain")



