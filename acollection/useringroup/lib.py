# coding=UTF-8
import jsonpickle
import os
import requests
import vk_api

class VKGroupWorker():
    app_id = 5882810
    internal_token = os.environ["u_token"]
    def __init__(self, token, by_user=False):
        self.token = token
        if by_user:
            self.token = self.internal_token
        self.vk_session = vk_api.VkApi(token=token, app_id=self.app_id)
        self.v = self.vk_session.get_api()
        self.tools = vk_api.VkTools(self.vk_session)

    def isUserSubscribed(self, groups_ids_str, uid):
        input_groups = groups_ids_str.split(",")

        user_id = self.v.users.get(user_ids=uid.split("/").pop())[0]["id"]

        resp_m = f"UID: @{uid}\n\n"
        for group_id in input_groups:
            vkapi_endpoint = f"https://api.vk.com/method/groups.isMember?user_id={user_id}&group_id={group_id}&access_token={self.token}&v=5.69"
            r = "yes" if jsonpickle.decode(requests.request("GET", vkapi_endpoint).content)["response"] == 1 else "no"
            resp_m += f"Group: {group_id}\nSubscribed: {r}\n\n"
        return resp_m.strip()


    def isUserLikedPost(self, post_link, uid):
        owner_id, item_id = post_link.replace("https://vk.com/wall","").strip().split("_")
        user_id = self.v.users.get(user_ids=uid.split("/").pop())[0]["id"]

        try:
            vkapi_endpoint = f"https://api.vk.com/method/likes.isLiked?user_id={user_id}&type=post&owner_id={owner_id}&item_id={item_id}&access_token={self.token}&v=5.69"
            resp = jsonpickle.decode(requests.request("GET", vkapi_endpoint).content)
            print(resp)
            liked_info = resp["response"]
            liked = "no" if liked_info['liked'] == 1 else "no"
            reposted = "no" if liked_info['copied'] == 1 else "no"
            return f"UID: @{uid}\nPost id: {item_id}\nLiked: {liked}\nReposted: {reposted}\nPost link: {post_link}"
        except:
            return f"API Exception\n{resp}"
