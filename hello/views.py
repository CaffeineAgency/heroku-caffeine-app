from django.shortcuts import render
from django.http import HttpResponse
import acollection as apis
from hello.lworkers.acollection_worker import *


# Create your views here.
def index(request):
    return render(request, 'index.html')

def acollection(request):
    url = "http://img1.pornreactor.cc/pics/post/Newhalf-Furry-Newhalf-%D1%81%D0%B5%D0%BA%D1%80%D0%B5%D1%82%D0%BD%D1%8B%D0%B5-%D1%80%D0%B0%D0%B7%D0%B4%D0%B5%D0%BB%D1%8B-4081553.jpeg"
    try:
        '''
        filename = download_file(url)
        response = upload_file(filename)
        return HttpResponse(response)
        '''
        ss = get_file_list("Newhalf")
        for post in ss:
            return HttpResponse(post.user)
    except YandexDiskException as ex:
        return HttpResponse(ex)



