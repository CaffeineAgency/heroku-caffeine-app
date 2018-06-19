import os
import requests
from vk_api import VkUpload


class GroupApiHooks:

    def __init__(self, gid):
        self.endpoint = "https://api.vk.com/method/"
        self.app_id = 5882810
        self.groupsec = os.environ[gid]
        self.internal_token = os.environ["u_token"]

    def send_message(self, uid, text):
        groupsec = self.groupsec
        req_url = f"{self.endpoint}messages.send?message={text}&peer_id={uid}"
        req_url += f"&access_token={groupsec}&v=5.80"
        requests.request("GET", req_url)

    def notify_creator(self, text, uid):
        self.send_message(307982226, "bot@Clyde > [from " + str(uid) + "] " + text)

    def upload_photo(self, peer, path_to_photo):
        groupsec = self.groupsec
        res = requests.get(f"{self.endpoint}photos.getMessagesUploadServer?peer_id={peer}"
                           f"&access_token={groupsec}&v=5.80")
        print(res.text)
        res = res.json()["response"]
        upload_url, album_id, user_id = res["upload_url"], res["album_id"], res["user_id"]
        res = requests.post(upload_url, data={"photo": requests.get(path_to_photo).raw})
        print(res.text)
        res = res.json()
        server, photo, hash = res["server"], res["photo"], res["hash"]
        res = requests.get(f"{self.endpoint}photos.saveMessagesPhoto?server={server}&"
                           f"photo={photo}&hash={hash}&access_token={groupsec}&v=5.80")
        print(res.text)
        res = res.json()
        oid, mid = res["oid"], res["mid"]
        vk_photo = 'photo{}_{}'.format(oid, mid)

        return vk_photo