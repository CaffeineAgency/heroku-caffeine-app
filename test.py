from vk_api import VkApi

from acollection.vk_api_pt.audio import VkAudio

vapi = VkApi(login="89535954236")
vapi.auth()
vkaudio = VkAudio(vapi)
tracks = []
for track in vkaudio.get_iter(0):
    print(track)
    break