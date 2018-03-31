import jsonpickle
from lxml import etree
import requests, lxml.html

class EVRLToApi:

    def __init__(self):
        self.baseurl = "https://evrl.to"
        self.newsurl = self.baseurl + "/news/"
        self.articlesurl = self.baseurl + "/articles/"
        self.guidesurl = self.baseurl + "/guides/"


    @staticmethod
    def jsondump(obj):
        return jsonpickle.encode(obj, unpicklable=False)


    def execute_registration(self, login, password):
        """
        login: reg_login
        password: reg_password
        """
        return {"error": "Not implemented yet"}


    def execute_login(self, login, password):
        """
        auth[login]: login
        auth[password]: password
        login_state: ? or SOFBAmi2RQhchcYm
        """
        return {"error": "Not implemented yet"}


    def get_mainpage(self, page=1):
        try:
            response = {
                "rid": 0,
                "has_next": None,
                "current_page": page,
                "last_page": None,
                "news": []
            }
            endurl = f"{self.baseurl}/?tab=mosaic_all&page={page}"
            docum = requests.get(endurl)
            dtree = lxml.html.fromstring(docum.content)
            pag_is = [x for x in dtree.cssselect(".mosaic_block") if "mosaic_other_news" not in x.attrib["class"]]
            for i, elem in enumerate(pag_is):
                # element.text_content() used to render text of element and all of its child
                info = elem.cssselect(".mosaic_info span")
                news = {
                    "title": elem.cssselect(".mosaic_title")[0].text_content().strip(),
                    "link": self.baseurl + elem.cssselect("a.mosaic_link")[0].attrib["href"]
                }
                tmp = elem.cssselect(".mosaic_description")
                news["description"] = tmp[0].text.strip() if tmp else ""
                tmp = elem.cssselect(".mosaic_poster")
                news["poster"] = "https://" + tmp[0].attrib["style"][19:].split('");')[0] if tmp else ""
                news["info"] = {
                    "views": int("0" + info[0].text_content()) if info else 0,
                    "comments": int("0" + info[1].text_content()) if info else 0,
                    "likes": int("0" + info[2].text_content()) if info else 0
                }
                response["news"].append(news)
            response["last_page"] = int(dtree.cssselect("ul.pagination li")[-1].text_content().strip())
            response["has_next"] = response["current_page"] != response["last_page"]
            return response
        except Exception as e:
            return {
                "rid": -2,
                "error": "; ".join(e.args)
            }


    def get_newspage(self, page=1):
        try:
            response = {
                "rid": 0,
                "has_next": None,
                "current_page": page,
                "last_page": None,
                "for_date": None,
                "news": []
            }
            endurl = f"{self.newsurl}/?page={page}"
            docum = requests.get(endurl)
            dtree = lxml.html.fromstring(docum.content)
            pag_is = [x for x in dtree.cssselect(".mosaic_block")]
            for i, elem in enumerate(pag_is):
                info = elem.cssselect(".mosaic_info span")
                news = {
                    "title": elem.cssselect(".mosaic_title")[0].text_content().strip(),
                    "link": self.baseurl + elem.cssselect("a.mosaic_link")[0].attrib["href"]
                }
                tmp = elem.cssselect(".mosaic_description")
                news["description"] = tmp[0].text.strip() if tmp else ""
                tmp = elem.cssselect(".mosaic_poster")
                news["poster"] = "https://" + tmp[0].attrib["style"][19:].split('");')[0] if tmp else ""
                news["info"] = {
                    "views": int("0" + info[0].text_content()) if info else 0,
                    "comments": int("0" + info[1].text_content()) if info else 0,
                    "likes": int("0" + info[2].text_content()) if info else 0
                }
                response["news"].append(news)
            response["last_page"] = int(dtree.cssselect("ul.pagination li")[-1].text_content().strip())
            response["has_next"] = response["current_page"] != response["last_page"]
            response["for_date"] = dtree.cssselect(".time-delimeter")[0].text_content().strip()
            return response
        except Exception as e:
            return {
                "rid": -2,
                "error": "; ".join(e.args)
            }


    def get_storiespage(self, page=1):
        try:
            response = {
                "rid": 0,
                "has_next": None,
                "current_page": page,
                "last_page": None,
                "news": []
            }
            endurl = f"{self.articlesurl}/?page={page}"
            docum = requests.get(endurl)
            dtree = lxml.html.fromstring(docum.content)
            pag_is = [x for x in dtree.cssselect(".mosaic_block")]
            for i, elem in enumerate(pag_is):
                info = elem.cssselect(".mosaic_info span")
                news = {
                    "title": elem.cssselect(".mosaic_title")[0].text_content().strip(),
                    "link": self.baseurl + elem.cssselect("a.mosaic_link")[0].attrib["href"]
                }
                tmp = elem.cssselect(".mosaic_description")
                news["description"] = tmp[0].text.strip() if tmp else ""
                tmp = elem.cssselect(".mosaic_poster")
                news["poster"] = "https://" + tmp[0].attrib["style"][19:].split('");')[0] if tmp else ""
                news["info"] = {
                    "views": int("0" + info[0].text_content()) if info else 0,
                    "comments": int("0" + info[1].text_content()) if info else 0,
                    "likes": int("0" + info[2].text_content()) if info else 0
                }
                news["tags"] = [x.text_content().strip() for x in elem.cssselect(".mosaic_tags span.label")]
                news["date"] = dtree.cssselect(".mosaic_time")[0].text_content().strip()
                response["news"].append(news)
            response["last_page"] = int(dtree.cssselect("ul.pagination li")[-1].text_content().strip())
            response["has_next"] = response["current_page"] != response["last_page"]
            return response
        except Exception as e:
            return {
                "rid": -2,
                "error": "; ".join(e.args)
            }


    def get_guidespage(self, page=1):
        try:
            response = {
                "rid": 0,
                "has_next": None,
                "current_page": page,
                "last_page": None,
                "guides": []
            }
            endurl = f"{self.guidesurl}/?page={page}"
            docum = requests.get(endurl)
            dtree = lxml.html.fromstring(docum.content)
            pag_is = [x for x in dtree.cssselect(".mosaic_block")]
            for i, elem in enumerate(pag_is):
                guides = {
                    "title": elem.cssselect(".mosaic_title")[0].text_content().strip(),
                    "link": self.baseurl + elem.cssselect("a.mosaic_link")[0].attrib["href"]
                }
                tmp = elem.cssselect(".mosaic_poster")
                guides["poster"] = "https://" + tmp[0].attrib["style"][19:].split('");')[0] if tmp else ""
                response["guides"].append(guides)
            response["last_page"] = int(dtree.cssselect("ul.pagination li")[-1].text_content().strip())
            response["has_next"] = response["current_page"] != response["last_page"]
            return response
        except Exception as e:
            return {
                "rid": -2,
                "error": "; ".join(e.args)
            }


    def get_article_content(self, link = None, article_id = None, named_link = None):
        try:
            if link:
                article_id, named_link = link.replace(self.articlesurl, "")[:-1].split("/")
            elif article_id and named_link:
                link = f"{self.articlesurl}/{article_id}/{named_link}/"
            else:
                return {
                    "rid": -1,
                    "error": "No article link or article_id and named_link given"
                }
            response = {
                "rid": 0,
                "link": link,
                "article_id": article_id,
                "named_link": named_link,
                "author": "",
                "date": "",
                "info": {},
                "content": "",
                "styles": [
                    "https://evrl.to/static/css/build_common.css"
                    "https://fonts.googleapis.com/css?family=Iceland"
                ],
                "scripts": [
                    "https://platform.twitter.com/widgets.js"
                    "https://evrl.to/static/js/build_vendor.js"
                    "https://evrl.to/static/js/build_evercore.js"
                ]
            }
            docum = requests.get(link)
            dtree = lxml.html.fromstring(docum.content)
            article_element = dtree.cssselect('[itemprop*=articleBody]')[0]
            response["content"] = etree.tostring(article_element).decode("utf8").strip()
            info = dtree.cssselect(".article-author span")
            response["author"] = dtree.cssselect(".article-author a")[0].text_content().strip()
            response["date"] = info.pop(0).attrib["datetime"]
            response["info"] = {
                "views": int("0" + info[0].text_content()) if info else 0,
                "comments": int("0" + info[2].text_content()) if info else 0,
                "likes": int("0" + info[1].text_content()) if info else 0
            }
            return response
        except Exception as e:
            return {
                "rid": -2,
                "error": "; ".join(e.args)
            }


    def get_story_content(self, link = None, article_id = None, named_link = None):
        try:
            if link:
                article_id, named_link = link.replace(self.articlesurl, "")[:-1].split("/")
            elif article_id and named_link:
                link = f"{self.articlesurl}/{article_id}/{named_link}/"
            else:
                return {
                    "rid": -1,
                    "error": "No article link or article_id and named_link given"
                }
            response = {
                "rid": 0,
                "link": link,
                "article_id": article_id,
                "named_link": named_link,
                "author": "",
                "date": "",
                "poster": "",
                "info": {},
                "content": "",
                "styles": [
                    "https://evrl.to/static/css/build_common.css"
                    "https://fonts.googleapis.com/css?family=Iceland"
                ],
                "scripts": [
                    "https://platform.twitter.com/widgets.js"
                    "https://evrl.to/static/js/build_vendor.js"
                    "https://evrl.to/static/js/build_evercore.js"
                ]
            }
            docum = requests.get(link)
            dtree = lxml.html.fromstring(docum.content)
            article_element = dtree.cssselect('[itemprop*=articleBody]')[0]
            response["content"] = etree.tostring(article_element).decode("utf8").strip()
            response["author"] = dtree.cssselect(".mg_author a")[0].text_content().strip()
            response["poster"] = dtree.cssselect(".mg_article_poster")[0].attrib["src"]
            info = dtree.cssselect(".mg_article_stat span")
            response["date"] = info.pop(0).attrib["datetime"]
            response["info"] = {
                "views": int("0" + info[0].text_content()) if info else 0,
                "comments": int("0" + info[2].text_content()) if info else 0,
                "likes": int("0" + info[1].text_content()) if info else 0
            }
            return response
        except Exception as e:
            return {
                "rid": -2,
                "error": "; ".join(e.args)
            }
