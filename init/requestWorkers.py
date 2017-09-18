def getGet(request, name):
    return request.GET.get(name)

def getPost(request, name):
    return request.POST.get(name)
