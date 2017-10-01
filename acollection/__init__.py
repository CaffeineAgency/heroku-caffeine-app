# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as soup

class Reactor(object):
    def __init__(self, url, blacklisted_tags=None):
        self.url = url
        if blacklisted_tags == None: blacklisted_tags = ["фэндомы", "artist", "секретные разделы", "игры", "r34",
                                                         "под катом продолжение"]
        self.b_t = blacklisted_tags

    def get_tag_posts(self, tag, num = 999):
        import re
        url = "{}/tag/{}/{}".format(self.url, tag, num)
        response = requests.get(url)
        post_list = soup(response.text, "html5lib").find("div", {"id": "post_list"})
        postContainers = post_list.find_all("div", {"class": "postContainer"})
        posts = []
        for postContainer in postContainers:
            post_top = postContainer.find("div", {"class": "post_top"})
            nick = post_top.find("div", {"class": "uhead"}).find("div", {"class": "uhead_nick"}).text
            avatar = post_top.find("div", {"class": "uhead"}).find("div", {"class": "uhead_nick"}).find("img").attrs["src"]
            taglist = [b.text.strip() for b in post_top.find("h2", {"class": "taglist"}).find_all("b")]
            taglist = [re.sub(r"(\(.*?\))", "", i) for i in taglist if i not in self.b_t]
            if post_top.find("div", {"class": "image"}) == None:
                continue
            imagelist = post_top.find("div", {"class": "image"}).find_all("a", {"rel": "prettyPhoto"})
            imagelist = [img.attrs["href"] for img in imagelist]
            if len(imagelist) == 0:
                imagelist = post_top.find("div", {"class": "image"}).find("img")
                imagelist = [img.attrs["src"] for img in imagelist]
            if len(imagelist) == 0:
                continue
            posts.append(Post(User(nick, avatar), taglist, imagelist))
        return posts

    def get_last_tag_page_num(self, tag):
        url = "{}/tag/{}".format(self.url, tag)
        response = requests.get(url)
        num = soup(response.text, "html5lib").find("div", {"class": "pagination_expanded"}).find("span", {"class": "current"}).text
        return int(num)


class User(object):
    def __init__(self, nick, avatar):
        self.nick = nick.strip()
        self.avatar = avatar


class Post(object):
    def __init__(self, user, tags_list, images_list):
        self.user = user
        self.tags_list = set(tags_list)
        self.images_list = images_list


class Response(object):
    def __init__(self, tag, host, offset):
        self.tag = tag
        self.host = host
        self.offset = offset
        self.lastpage = 999999
        self.posts = []
        self.time_taken = "0 sec."
