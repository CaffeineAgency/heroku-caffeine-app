from django.http import StreamingHttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponse
import acollection as apis
from hello.lworkers import collect
from hello.lworkers.acollection_worker import *
from init.requestWorkers import getGet


def index(request):
    from django.template import TemplateDoesNotExist
    try:
        return render_to_response('index.html')
    except TemplateDoesNotExist as ex:
        import jsonpickle
        return HttpResponse(jsonpickle.encode(ex, unpicklable=False, max_depth=10))


def acollection(request):
    mode = getGet(request, "mode")
    if mode == "ubl":
        url = getGet(request, "u")
        filename = getGet(request, "f")
        upload_file_by_link(url, filename)
        return HttpResponse(upload_file_by_link(url, filename), content_type="text/plain")
    elif mode == "ubf":
        url = getGet(request, "u")
        return HttpResponse(download_and_upload_file(url), content_type="text/plain")
    elif mode == "col":
        collect.main()
    elif mode == "stream":
        return StreamingHttpResponse([x for x in range(500000)])
    else:
        return HttpResponse("""
        СПРАВКА:\n
        Существует три мода работы сервиса:\n
        \t'uploading file by link'
        \t\tМетод: GET
        \t\tВходные данные:
        \t\t\tmode=ubl
        \t\t\tu=<url>
        \t\t\tf=<filename> - можно не указывать
        \t'download and upload file'
        \tПозволяет обойти ограничение яндекса на файлы, запрещённые на территории РФ. Не загружайте большие файлы.
        \t\tМетод: GET
        \t\tВходные данные:
        \t\t\tmode=ubf
        \t\t\tu=<url>
        \t'collect.main'
        \tПока в разработке.
        """.encode("cp1251"), content_type="text/plain")



