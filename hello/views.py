from django.shortcuts import render
from django.http import HttpResponse
import acollection as apis
from hello.lworkers.acollection_worker import *


# Create your views here.
def index(request):
    return render(request, '../index.html')

def acollection(request):
    try:
        response = ""
        ss = get_file_list("r34")
        for post in ss:
            for image in post.images_list:
                try:
                    url = image
                    filename = download_file(url)
                    response += "{}<br><br><br>\n\n\n".format(upload_file(filename))
                except YandexDiskException as ex:
                    continue
        return HttpResponse(response)
    except ConnectionError as ex:
        return HttpResponse(ex)



