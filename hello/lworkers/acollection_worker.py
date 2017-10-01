import init.requestWorkers as rw
from acollection import Response, Reactor
from ydapi.YandexDiskRestClient import YandexDiskRestClient
from ydapi.YandexDiskException import YandexDiskException
from urllib.parse import unquote
import requests, shutil, os

api = YandexDiskRestClient("AQAAAAAMTrBzAARbbEhJbcQgn0dDg-Nag1ykG7o")


def download_file(url):
    try:
        url = unquote(url)
        filename = url.split("/").pop()
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        return filename
    except Exception as exp:
        raise exp


def upload_file(filename):
    try:
        path = "/Herokuer/" + filename
        return api.upload_file_and_remove(filename, path)
    except YandexDiskException as exp:
        raise exp


def get_file_list(tag="r34", offset=1, as_json=False):
    response = Response(tag, "http://pornreactor.cc/", offset)
    pornreactor = Reactor(response.host)
    pn = pornreactor.get_last_tag_page_num(response.tag)
    response.lastpage = pn
    for i in range(pn, pn - 10 * response.offset, -1):
        posts = pornreactor.get_tag_posts(response.tag, i)
        response.posts += posts
    if as_json:
        import jsonpickle
        return jsonpickle.encode(response, unpicklable=False)
    else:
        return response.posts