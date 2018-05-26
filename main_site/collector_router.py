# coding=utf-8
from flask import render_template
from extensions import getGet

import acollection.deviantartlib.api as dapi
import acollection.evrltolib.api as evrlapi
import acollection.reactorlib.api as reapi
import acollection.ruminelib.api as rapi
from acollection.ydapi.yandexdisk_worker import *


class ApiRouter:
    def __init__(self, cmdname, request):
        cmdlist = {
            "yagui": self.yandexgui,
            "reactorgui": self.reactorgui,
            "ubl": self.yandex_upload_file_by_link,
            "chk": self.async_operation_checker,
            "rumine": self.rumine_forum_parser,
            "reactorparser": self.pornreactor_tag_parser,
            "evrltolib": self.evrlto_parser,
            "deviantart": self.deviantart_worker,
        }

        self.request = request
        self.command = cmdlist[cmdname] if cmdlist.get(cmdname) else self.info

    def execute(self):
        return self.command()

    def yandexgui(self):
        return render_template('yandexworker.html'), "text/html"

    def reactorgui(self):
        return render_template('reactorgallery.html'), "text/html"

    def yandex_upload_file_by_link(self):
        url = getGet(self.request, "u")
        filename = getGet(self.request, "f")
        id = upload_file_by_link(url, filename)
        return id, "text/plain"

    def async_operation_checker(self):
        id = getGet(self.request, "id")
        return check_async_operation(id), "text/plain"

    def rumine_forum_parser(self):
        rq = {
            "threadId": getGet(self.request, "threadId"),
            "pagenum": getGet(self.request, "pagenum")
        }
        api = rapi.RuMineApi(request=rq)
        return api.get_comments(), "application/json"

    def pornreactor_tag_parser(self):
        rq = {
            "tag": getGet(self.request, "tag"),
            "page": getGet(self.request, "page")
        }
        return reapi.ReactorApi().get_images(request=rq), "application/json"

    def evrlto_parser(self):
        api = evrlapi.EVRLToApi()
        response = {}
        link = getGet(self.request, "link")
        article_id = getGet(self.request, "article_id")
        named_link = getGet(self.request, "named_link")
        page = getGet(self.request, "page")

        type = getGet(self.request, "type")
        if type == "main":
            response = api.get_mainpage(page if page else 1)
        elif type == "news":
            response = api.get_newspage(page if page else 1)
        elif type == "stories":
            response = api.get_storiespage(page if page else 1)
        elif type == "guides":
            response = api.get_guidespage(page if page else 1)
        elif type == "article":
            response = api.get_article_content(link, article_id, named_link)
        elif type == "story":
            response = api.get_story_content(link, article_id, named_link)

        return api.jsondump(response), "application/json"

    def deviantart_worker(self):
        do = getGet(self.request, "do")
        if do == "rip":
            url = getGet(self.request, "url")
            if url:
                api = dapi.DeviantRipperApi(url)
                return api.get_gallery_of_author(), "application/json"
        return "No work specified", "text/plain"

    def info(self):
        return """
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
                    'evrlto api' - API для сайта EVRL{dot}to.
                        Метод: GET
                        Входные данные:
                            mode=evrltolib
                            type=<one of [main, news, stories, guides] or [article, story]>
                            // Далее всё зависит от type:
                                // Верхние типы
                                main:       - Возвращает новости с главной страницы сайта Ссылки на истории передавать в ::article
                                news:       - Вовзращает новости с раздела новостей Ссылки на истории передавать в ::article
                                stories:    - Возвращает т.н. "Истории". Ссылки на истории передавать в ::story
                                guides:     - Возвращает гайды из раздела гайдов сайта Ссылки на истории передавать в ::article
                                    page=<pagenum> - Можно не указывать
                                // Нижние типы
                                article:
                                story:
                                    // Tip: link - обязателен, если не указаны article_id и named_link, и наоборот
                                    link=<link>
                                    article_id=<aid>
                                    named_link=<nl>
                """, "text/plain"
