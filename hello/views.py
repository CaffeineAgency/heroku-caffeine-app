from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'index.html')

def test(request):
    import init.requestWorkers as rw
    from ydapi.YandexDiskRestClient import YandexDiskRestClient
    from ydapi.YandexDiskException import YandexDiskException
    from urllib.parse import unquote
    import requests, shutil, os

    api = YandexDiskRestClient("AQAAAAAMTrBzAARbbEhJbcQgn0dDg-Nag1ykG7o")
    try:
        url = "http://img1.pornreactor.cc/pics/post/Newhalf-Furry-Newhalf-%D1%81%D0%B5%D0%BA%D1%80%D0%B5%D1%82%D0%BD%D1%8B%D0%B5-%D1%80%D0%B0%D0%B7%D0%B4%D0%B5%D0%BB%D1%8B-4081553.jpeg"
        url = unquote(url)
        path = "Newhalf-Furry-Newhalf-4081553.jpeg"
        (dirname, filename) = os.path.split(url)
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        #path = "/Herokuer/" + path

        return HttpResponse(api.upload_file(filename, path))
    except YandexDiskException as exp:
        return HttpResponse(exp)



