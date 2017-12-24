# -*- coding: utf-8 -*-
from acollection.deviantartlib.models import WorkerTask


class DeviantRipperApi:
    def __init__(self, url):
        self.url = str(url)

    def get_gallery_of_author(self):
        task = WorkerTask(self.url)
        return task.get_urls()