# encoding=utf-8
import shutil
import time

import lxml.html
import requests

from acollection.exts.Downloader import Downloader


class NozomiApi:

    plink = "http://nuark.xyz/proxy.php?h&l="
    images = []

    def main(self, tag=None, maxpage=10, proxy=False):
        self.plink = self.plink if proxy else ""
        base = "https://nozomi.la"
        ot = 1
        p = 0
        self.tmpdir = "./tmp_" + str(time.time()).replace(".", "") + "/"
        for i in range(ot, maxpage):
            try:
                html = requests.get(f"{self.plink}{base}/{'index' if not tag else 'tag/' + tag}-{i}.html").text
                yield self.parse(base, html)
            except:
                continue
        zipname = self.tmpdir[2:-1] + ".zip"
        shutil.make_archive(zipname, "zip", self.tmpdir, self.tmpdir)
        print(zipname)
        print(requests.post("http://vaix.ru/upload?file=" + zipname, files=zipname).content)
        print(self.tmpdir + zipname)
        print(requests.post("http://vaix.ru/upload?file=" + zipname, files=self.tmpdir + zipname).content)



    def parse(self, base, html):
        root = lxml.html.fromstring(html)
        root.make_links_absolute(base)
        posts = [x.attrib["href"] for x in root.cssselect("div.thumbnail-div a")]
        for post in posts:
            post = post.split("#")[0]
            try:
                print("Dealing with post: " + post)
                html = requests.get(self.plink + post).text
                root = lxml.html.fromstring(html)
                root.make_links_absolute(base)
                image = root.cssselect("div.post img")[0].attrib["src"]
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
                Downloader().download(image, rname=True, directory=self.tmpdir)
                yield "This post done: " + post
            except Exception as e:
                yield "Error with post: " + post + str(e)
                continue

    if __name__ == '__main__':
        tag = input("Грузим тэг?\n(https://nozomi.la/tag/{ТЭГ}-1.html)\n(можно оставить пустым)\n>> ").strip()
        if len(tag.strip()) == 0:
            tag = None
        plink = plink if input(
            "Проксируем?[y/std: n]\n(мб медленно, зато в обход блокировок)\n>> ").lower() == "y" else ""
        main(tag)
