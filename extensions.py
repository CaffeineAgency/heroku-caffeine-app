def getGet(request, name):
    return request.args.get(name)

def getPost(request, name):
    return request.form.get(name)

def getVal(request, name):
    return request.values.get(name)

def getData(request):
    return request.json
