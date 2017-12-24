# -*- coding: utf-8 -*-
import jsonpickle
from bs4 import BeautifulSoup as bs
import requests

class WorkerTask:
    URL = "https://www.deviantart.com/dapi/v1/gallery/"
    def __init__(self, url):
        if not url.startswith("https://"):
            raise Exception("Author's gallery URL should starts with \"https://\"")
        elif "deviantart.com/gallery/" not in url:
            raise Exception("Author's gallery URL should contains \"deviantart.com/gallery/\"")
        self.MAINURL = url
        self.Author = url.replace("http://", "").replace("https://", "").split('.')[0]

    def get_urls(self):
        urls = []
        hasmore = True
        offset = 0
        conn = requests.Session()
        conn.headers.update({"UserAgent": "Maxthon 5"})
        resp = conn.get(url=self.MAINURL)
        doc = bs(resp.content, "html5lib")
        mainscript = doc.select('script[type="text/javascript"]')[::-1][8]
        mainscript = str(mainscript).split("=")[2].split(";")[0]
        mainjson = jsonpickle.decode(mainscript)
        RID = mainjson["bilogger"]["requestid"]
        CSRF = mainjson["csrf"]
        GID = doc.select("#gmi-GalleryEditor")[0].attrs["gmi-itemid"]
        data = {
            "username": self.Author,
            "limit": "24",
            "_csrf": CSRF,
            "dapiIid": RID,
            "offset": 0
        }
        self.URL += GID
        while hasmore:
            resp = conn.post(url=self.URL, data=data)
            got = resp.text
            respjson = jsonpickle.decode(got)
            for i in range(len(respjson["dapi"]["metadata"])):
                urls.append((respjson["dapi"]["metadata"][f".{i}"]["alt"], respjson["dapi"]["metadata"][f".{i}"]["src"]))
            hasmore = respjson["content"]["has_more"]
            offset += 24
            data["offset"] = str(offset)
        return jsonpickle.encode(urls, unpicklable=False)