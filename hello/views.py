from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'index.html')

def test(request):
    import init.requestWorkers as rw
    from ydapi.YandexDiskRestClient import YandexDiskRestClient
    from ydapi.YandexDiskException import YandexDiskException

    api = YandexDiskRestClient("47d8dbf144ce417e8eaa543d94d5f193")
    try:
        disk = api.get_disk_metadata()
        rsp = "total space of disk = " + str(disk.total_space)
        rsp += "<br>used spase of disk = " + str(disk.used_space)
        return HttpResponse(rsp)
    except YandexDiskException as exp:
        return HttpResponse(exp)



