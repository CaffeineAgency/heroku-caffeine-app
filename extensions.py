from flask import request

def getGet(request, name):
    return request.args.get(name)

def getPost(request, name):
    return request.POST.get(name)

def getData(request):
    return request.json
