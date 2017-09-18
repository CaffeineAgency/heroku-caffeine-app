from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'index.html')

def test(request):
    import init.requestWorkers as rw
    from ydapi.YandexDiskRestClient import YandexDiskRestClient
    from ydapi.YandexDiskException import YandexDiskException

    api = YandexDiskRestClient("AQAAAAAMTrBzAARbbEhJbcQgn0dDg-Nag1ykG7o")
    try:
        url = rw.getGet(request, "iu")
        path = rw.getGet(request, "nm")
        #path = "/Herokuer/" + rw.getGet(request, "nm")
        api.upload_file_from_url(url, path)
        return HttpResponse("Uploading...")
    except YandexDiskException as exp:
        return HttpResponse(exp)



