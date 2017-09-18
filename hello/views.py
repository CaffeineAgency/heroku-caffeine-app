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
        api.create_folder("/dwm")
        api.upload_file_from_url(from_url="https://mp3.life/files/2bff37c42ca388b1.mp3", path_to="/dwm")
        return HttpResponse(api.get_list_of_all_files())
    except YandexDiskException as exp:
        return HttpResponse(exp)



