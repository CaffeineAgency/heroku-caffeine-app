# -*- coding: utf-8 -*-
import codecs
import bs4 as bs
from bs4 import Comment
import base64
from .models import Post, Response
import jsonpickle
import requests


class RuMineApi():
    def __init__(self, login=None, password=None, request=None):
        self.pagenum = 9999999999999
        self.base_url = "https://ru-minecraft.ru"
        self.login = login
        self.password = password
        self.request = request

    def prepare_uri(self, request=None):
        if not request:
            if self.request:
                request = self.request
            else:
                raise Exception("No request dict passed")
        if request["threadId"] is None:
            raise Exception("No threadId passed")
        else:
            try:
                self.threadId = int(request["threadId"])
            except:
                raise Exception("No threadId passed")
        if request["pagenum"] is None:
            self.pagenum = 9999999999999
        else:
            try:
                self.pagenum = request["pagenum"]
            except:
                pass
        return "{}/forum/showtopic-{}/page-{}/".format(self.base_url, self.threadId, self.pagenum)

    def parse_data(self, soup):
        posts = []
        for item in soup.find_all('li', class_="msg"):
            pid = item.select_one(".msgInfo a").text.replace("#", "")
            sender = item.select_one(".msgAutorInfo .autorInfo p > a").text
            stri = item.select_one(".msgText td > div").encode('utf-8')
            posts.append(Post(pid, sender, stri))
        return Response(posts)

    def get_comments(self, url=None):
        try:
            if self.request is not None:
                url = self.prepare_uri(self.request)
            source = requests.get(url)
            source = codecs.decode(source.content, "windows-1251")
            soup = bs.BeautifulSoup(source, "html5lib")
            # Sanitize HTML
            [itm.nextSibling.extract() for itm in soup.findAll("div", class_="clr")]
            [likr.extract() for likr in soup.findAll("div", class_="EditMsgView")]
            [comment.extract() for comment in soup.findAll(text=lambda text: isinstance(text, Comment))]
            [spmark.extract() for spmark in soup.findAll("div", class_="title_spoiler")]
            for spler in soup.findAll("div", class_="text_spoiler"): del(spler['style'])
            rarray = self.parse_data(soup)
            narray = []
            for post in rarray.posts:
                _post = post
                _post.text = codecs.decode(self.parse_data(soup).posts.pop().text, "UTF-8")
                narray.append(_post)
            rarray.posts = narray

            return jsonpickle.encode(rarray, unpicklable=False)
        except Exception as ex:
            return jsonpickle.encode(dict(error=ex.args), unpicklable=False)
