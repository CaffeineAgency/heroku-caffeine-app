from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting


# Create your views here.
def index(request):
    return render(request, 'index.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})


def test(request):
    import init.requestWorkers as rw
    import vk_api
    vk_session = vk_api.VkApi(token="ed12702994b221ed2cef5e4dfacaf4106a47285a41b5f9605f8f54930e82e1ea578bd62549b795e588fa7")
    vk_session.authorization()
    api = vk_session.get_api()
    tools = vk_api.VkTools(vk_session)

    owner = '148147627'
    items = tools.get_all('wall.get', 100, {'owner_id': int("-" + owner)})["items"]
    strhtml = ''
    for item in items:
        if not "attachments" in item:
            continue
        attachments = item["attachments"]
        for attachment in attachments:
            if attachment["type"] != "photo":
                continue
            photo = attachment["photo"]
            if ("photo_2560" in photo):
                url = photo["photo_2560"]
            elif ("photo_1280" in photo):
                url = photo["photo_1280"]
            elif ("photo_807" in photo):
                url = photo["photo_807"]
            elif ("photo_604" in photo):
                url = photo["photo_604"]
            else:
                continue
            strhtml += '<img src="' + url.replace(' ', '/') + '"/><br>'

    return HttpResponse(strhtml)

