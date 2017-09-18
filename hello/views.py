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
    return HttpResponse(str(request.body) + " || " + str(request.data) + " || " + str(request.GET) + " || " + str(request.POST))
    """
    import vk_api
    client_id = '5882810'
    client_sec = 'umeTZX5ykJVPyNsQSlzf'
    vk_session = vk_api.VkApi(token="e5fe3e55c448969c1bb62a51429b409863d46199f346401508e01efae41fcaf4bc52be0aded49cf736fd3")
    perm = "messages,friends,audio,offline,groups,wall"
    vk_session = vk_api.VkApi(email, password, auth_handler=two_factor_handler)
    "_""
    vk_session.authorization()
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
    """

