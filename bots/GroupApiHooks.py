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
        req_url = f"{self.endpoint}messages.send?message={text}&user_id={uid}&access_token={groupsec}&v=5.73"
        requests.request("GET", req_url)

    def users_get(self, *ids):
        groupsec = self.groupsec
        req_url = f"{self.endpoint}users.get?user_ids={','.join(ids[:1000])}&access_token={groupsec}&v=5.73"
        response = requests.request("GET", req_url).json()
        text = ""
        for i, user in enumerate(response["response"]):
            text += f"{i}. {user['first_name']} + {user['last_name']}".strip() + "\n"
        return text

    @staticmethod
    def notify_creator(text):
        GroupApiHooks().send_message(307982226, "bot@Clyde > " + text)