# encoding=utf-8
import shutil
import time
from collections import Counter

import lxml.html
import os
import requests

from acollection.exts.Downloader import Downloader


class NozomiApi:

    plink = "http://nuark.xyz/proxy.php?h&l="
    images = []

    def main(self, tag=None, maxpage=10, proxy=False):
        maxpage += 1
        plink = self.plink if proxy else ""
        base = "https://nozomi.la"
        tmpdir = os.getcwd() + "/tmp_" + str(time.time()).replace(".", "") + "/"
        if not os.path.exists(tmpdir):
            os.mkdir(tmpdir)
        for i in range(1, maxpage):
            try:
                html = requests.get(f"{self.plink}{base}/{'index' if not tag else 'tag/' + tag}-{i}.html").text
                root = lxml.html.fromstring(html)
                root.make_links_absolute(base)
                posts = [x.attrib["href"] for x in root.cssselect("div.thumbnail-div a")]
                for x, post in enumerate(posts):
                    post = post.split("#")[0]
                    try:
                        print("Dealing with post: " + post)
                        html = requests.get(self.plink + post).text
                        root = lxml.html.fromstring(html)
                        root.make_links_absolute(base)
                        image = root.cssselect("div.post img")[0].attrib["src"]
                        self.images.append(image)
                        sidebar = root.cssselect("div.sidebar")[0]
                        chrs, series, artist, tags, uls = [], [], [], [], sidebar.cssselect("ul")
                        for i, span in enumerate(sidebar.cssselect("span.title")):
                            title = span.text.strip()
                            if title == "Characters":
                                chrs = [x.text for x in uls[i].cssselect("li a")]
                            elif title == "Series":
                                series = [x.text for x in uls[i].cssselect("li a")]
                            elif title == "Artist":
                                artist = [x.text for x in uls[i].cssselect("li a")]
                            elif title == "Tags":
                                tags = [x.text for x in uls[i].cssselect("li a")]
                        Downloader().download(image, rname=True, directory=tmpdir)
                        yield str(x) + " This post done: " + post + "\n"
                    except Exception as e:
                        yield str(x) + " Error with post: " + post + " " + str(e) + "\n"
                        continue
            except:
                continue
            c = Counter(self.images)
            if c.most_common(1)[0][1] > 1:
                break
        fname = shutil.make_archive(tmpdir[2:-1], "zip", tmpdir)
        files = {"file": (tag + "_" + str(maxpage) + "_" + tmpdir[5:-1] + ".zip", open(fname, "rb"), "application/zip")}
        yield "Archive done: " + fname + "\n"
        try:
            rsp = requests.post("http://vaix.ru/upload", files=files).json()["file"][0]
            yield "Response: path-> " + rsp["path"] + "\n"
            yield "Response: path_delete-> " + rsp["path_delete"]
        except Exception as e:
            yield "Error with upload: " + str(e)
