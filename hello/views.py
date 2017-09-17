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
    import vk_api
    return HttpResponse('TEST<b>BOLD</b><br>TEST')

