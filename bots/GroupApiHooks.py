import os
import random
import string

import requests
import urllib.request as request
from vk_api import VkUpload


class GroupApiHooks:

    def __init__(self, gid):
        self.endpoint = "https://api.vk.com/method/"
        self.app_id = 5882810
        self.groupsec = os.environ[gid]
        self.internal_token = os.environ["u_token"]
        self.mapi_params = {
            "v": "5.80",
            "access_token": self.groupsec
        }

    def users_get(self, *ids):
        ids = [str(x) for x in ids[:1000]]
        params = {
            **self.mapi_params,
            "user_ids": ",".join(ids)
        }
        req_url = f"{self.endpoint}users.get"
        response = requests.get(req_url, params).json()
        text = ""
        for i, user in enumerate(iterable=response["response"], start=1):
            text += f"{i}. {user['first_name']} {user['last_name']}".strip() + "\n"
        return text.strip()

    def send_message(self, uid, text, params=None):
        if params is None:
            params = {}
        params = {
            **self.mapi_params,
            "message": text,
            "peer_id": uid,
            **params,
        }
        params["random_id"] = "".join([str(ord(c)) for c in str(params)])
        print("bot@Mainframe > sending message with parameters:", params)
        req_url = f"{self.endpoint}messages.send"
        requests.get(req_url, params)

    def notify_creator(self, text, uid):
        self.send_message(307982226, "bot@Clyde > [from " + str(uid) + "] " + text)

    def upload_photo(self, photo_url, peer=307982226):
        def downloadImage(image):
            randomName = "".join([random.choice(string.ascii_letters) for x in range(15)]) + ".png"
            fullfilename = os.path.join("./", randomName)
            request.urlretrieve(image, fullfilename)
            return fullfilename

        params = {
            **self.mapi_params,
            "peer_id": peer,
        }
        res = requests.get("https://api.vk.com/method/photos.getMessagesUploadServer", params)
        res = res.json()["response"]
        upload_url, album_id = res["upload_url"], res["album_id"]
        image = downloadImage(photo_url)
        with open(image, "rb") as f_image:
            res = requests.post(upload_url, files={"photo": (image.split("/")[-1], f_image)})
            res = res.json()
        server, photo, _hash = res["server"], res["photo"], res["hash"]
        params = {
            **self.mapi_params,
            "server": server,
            "photo": photo,
            "hash": _hash,
            "album_id": album_id
        }
        res = requests.get("https://api.vk.com/method/photos.saveMessagesPhoto", params)
        res = res.json()["response"][0]
        owner_id, media_id = res["owner_id"], res["id"]
        vk_photo = "photo{}_{}".format(owner_id, media_id)
        return vk_photo