# -*- coding: utf-8 -*-
import codecs
import bs4 as bs
from bs4 import Comment
import base64
from .models import Post, Response
import jsonpickle
import requests


class ReactorApi():
    def __init__(self):
        self.base_url = "http://joyreactor.cc"

    def prepare_uri(self, request):
        if request["tag"] is None:
            raise Exception("No tag passed")
        tag = request["tag"].replace(" ", "+")
        page = "" if request["page"] == "latest" else f'/{request["page"]}'
        return f"{self.base_url}/tag/{tag}{page}"

    def parse_data(self, soup):
        posts = []
        lp = int(next(soup.select_one("div.pagination_expanded").children).text)
        if lp is None:
            raise Exception("404 HTTP Error catched!")
        for item in soup.select("div.postContainer"):
            image = item.select_one("img.avatar")
            author = dict(avatar=image.attrs["src"], nick=image.attrs["alt"])
            images = []
            for img in item.select("img"):
                if img.has_attr("width") or img.has_attr("height"):
                    pieces = img.attrs["src"].replace("http://", "").split("/")
                    domen = pieces[0]
                    file = pieces.pop()
                    link = f"http://{domen}/pics/post/full/{file}"
                    images.append(link)
            tags = [tag.text.strip() for tag in item.select(".taglist b")]
            posts.append(Post(author, images, tags))
        return Response(lp, posts)

    def get_images(self, url=None, request=None):
        try:
            if url is None:
                if request is None:
                    raise Exception("Not valid request passed")
                url = self.prepare_uri(request)
            source = requests.get(url)
            source = codecs.decode(source.content, source.encoding)
            soup = bs.BeautifulSoup(source, "html5lib")
            rarray = self.parse_data(soup)
            return jsonpickle.encode(rarray, unpicklable=False)
        except Exception as ex:
            return jsonpickle.encode(dict(error=ex.args), unpicklable=False)