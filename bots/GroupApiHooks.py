import os
import requests
from vk_api import VkUpload


class GroupApiHooks:

    def __init__(self, gid):
        self.endpoint = "https://api.vk.com/method/"
        self.app_id = 5882810
        self.groupsec = os.environ[gid]
        self.internal_token = os.environ["u_token"]

    def users_get(self, *ids):
        groupsec = self.groupsec
        ids = [str(x) for x in ids[:1000]]
        req_url = f"{self.endpoint}users.get?user_ids={','.join(ids)}&access_token={groupsec}&v=5.73"
        response = requests.request("GET", req_url).json()
        text = ""
        for i, user in enumerate(response["response"]):
            text += f"{i}. {user['first_name']} + {user['last_name']}".strip() + "\n"
        return text.strip()

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
                           f"&access_token={groupsec}&v=5.80").json()["response"]
        upload_url = res["upload_url"]
        print(upload_url)
        print("Loading image...", end=" ")
        with requests.get(path_to_photo, stream=True) as image:
            files = {'file1': image.raw}
            res = requests.post(upload_url, files=files).json()
            server, photo, _hash = res["server"], res["photo"], res["hash"]
            print(res, server, photo, _hash)
            res = requests.get(f"{self.endpoint}photos.saveMessagesPhoto?server={server}&"
                               f"photo={photo}&hash={_hash}&access_token={groupsec}&v=5.80").json()
            print(res)
            oid, mid = res["owner_id"], res["id"]
            print(oid, mid)
            vk_photo = 'photo{}_{}'.format(oid, mid)

        return vk_photo