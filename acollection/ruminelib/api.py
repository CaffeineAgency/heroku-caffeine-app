# -*- coding: utf-8 -*-
import codecs
import bs4 as bs
from bs4 import Comment
import base64
from .models import Post, Response
import jsonpickle
import requests


class RuMineApi():
    def __init__(self, request, login=None, password=None):
        self.pagenum = 9999999999999
        self.base_url = "https://ru-minecraft.ru"
        self.login = login
        self.password = password
        self.request = request
        if not self.request["threadId"]:
            raise Exception("No threadId passed")
        self.pagenum = 9999999999999 if not self.request["pagenum"] else self.request["pagenum"]
        self.threadId = int(self.request["threadId"])

    def parse_data(self, soup):
        posts = []
        for item in soup.select("li.msg"):
            pid = item.select_one(".msgInfo a").text.replace("#", "")
            sender = item.select_one(".msgAutorInfo .autorInfo p > a").text
            stri = str(item.select_one(".msgText td > div"))
            posts.append(Post(pid, sender, stri))
        return Response(posts)

    def get_comments(self):
        try:
            url = f"{self.base_url}/forum/showtopic-{self.threadId}/page-{self.pagenum}/"
            source = requests.get(url)
            source = codecs.decode(source.content, source.encoding)
            soup = bs.BeautifulSoup(source, "html5lib")
            # Sanitize HTML
            [itm.nextSibling.extract() for itm in soup.findAll("div", class_="clr")]
            [likr.extract() for likr in soup.findAll("div", class_="EditMsgView")]
            [comment.extract() for comment in soup.findAll(text=lambda text: isinstance(text, Comment))]
            [spmark.extract() for spmark in soup.findAll("div", class_="title_spoiler")]
            for spler in soup.findAll("div", class_="text_spoiler"): del(spler['style'])
            rarray = self.parse_data(soup)
            return jsonpickle.encode(rarray, unpicklable=False)
        except Exception as ex:
            return jsonpickle.encode(dict(errors=ex.args), unpicklable=False)
