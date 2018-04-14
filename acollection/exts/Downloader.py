import os
import shutil

import requests
import time


class Downloader:
    def escape_filename(self, string):
        banned_chars = '"|     :*?\/\n\r\t'
        for char in banned_chars:
            string = string.replace(char, "")
        return string

    def download(self, link, filename=None, directory="./downloads/", rname=False,):
        if rname:
            filename = str(time.time()).replace(".", "") + link.split(".")[-1]
        elif not filename:
            filename = link.split("/").pop().split("?")[0]
        else:
            filename = self.escape_filename(filename)
        filereq = requests.get(link, stream=True)
        if not os.path.exists(directory):
            os.mkdir(directory)
        if os.path.exists(directory + filename):
            if os.stat(directory + filename).st_size == int(filereq.headers["content-length"]):
                print("File already downloaded: " + directory + filename)
                return
        with open(directory + filename, "wb") as receive:
            shutil.copyfileobj(filereq.raw, receive)
        del filereq
        print("Downloaded file: " + directory + filename)
