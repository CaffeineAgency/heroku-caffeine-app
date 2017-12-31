# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render_to_response

import acollection.deviantartlib.api as dapi
import acollection.reactorlib.api as reapi
import acollection.ruminelib.api as rapi
from acollection.ydapi.yandexdisk_worker import *
from init.extensions import getGet


class ApiRouter:
    def __init__(self, cmdname, request):
        cmdlist = {
            "yagui": self.yandexgui,
            "reactorgui": self.reactorgui,
            "ubl": self.yandex_upload_file_by_link,
            "chk": self.async_operation_checker,
            "rumine": self.rumine_forum_parser,
            "reactorparser": self.pornreactor_tag_parser,
            "deviantart": self.deviantart_worker,
        }

        self.request = request
        self.command = cmdlist[cmdname] if cmdlist.get(cmdname) else self.info

    def execute(self):
        return self.command()

    def yandexgui(self):
        return render_to_response('yandexworker.html')

    def reactorgui(self):
        return render_to_response('reactorgallery.html')

    def yandex_upload_file_by_link(self):
        url = getGet(self.request, "u")
        filename = getGet(self.request, "f")
        id = upload_file_by_link(url, filename)
        return HttpResponse(id)

    def async_operation_checker(self):
        id = getGet(self.request, "id")
        return HttpResponse(check_async_operation(id))

    def rumine_forum_parser(self):
        rq = dict()
        rq["threadId"] = getGet(self.request, "threadId")
        rq["pagenum"] = getGet(self.request, "pagenum")
        rq["b64"] = getGet(self.request, "b64")
        api = rapi.RuMineApi(request=rq)
        return HttpResponse(api.get_comments())

    def pornreactor_tag_parser(self):
        rq = dict()
        rq["tag"] = getGet(self.request, "tag")
        rq["page"] = getGet(self.request, "page")
        return HttpResponse(reapi.ReactorApi().get_images(request=rq))

    def deviantart_worker(self):
        do = getGet(self.request, "do")
        if do == "rip":
            url = getGet(self.request, "url")
            if url:
                api = dapi.DeviantRipperApi(url)
                return HttpResponse(api.get_gallery_of_author())
        return HttpResponse("No work specified")

    def info(self):
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
