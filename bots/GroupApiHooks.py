import os
import requests


class GroupApiHooks:

    def __init__(self, gid):
        self.endpoint = "https://api.vk.com/method/"
        self.app_id = 5882810
        self.groupsec = os.environ[gid]
        self.internal_token = os.environ["u_token"]

    def send_message(self, uid, text):
        groupsec = self.groupsec
        req_url = f"{self.endpoint}messages.send?message={text}&peer_id={uid}&access_token={groupsec}&v=5.73"
        requests.request("GET", req_url)

    def notify_creator(self, text, uid):
        self.send_message(307982226, "bot@Clyde > [from " + str(uid) + "] " + text)