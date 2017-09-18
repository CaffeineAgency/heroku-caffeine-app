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
        disk = api.upload_file_from_url(from_url="http://v2.svekolnik.com/download.php?path=/p38389/p38389_720p.mp4", path_to="/")
        rsp = "total space of disk = " + str(disk.total_space)
        rsp += "<br>used spase of disk = " + str(disk.used_space)
        return HttpResponse(rsp)
    except YandexDiskException as exp:
        return HttpResponse(exp)



