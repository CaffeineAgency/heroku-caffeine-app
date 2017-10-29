# -*- coding: utf-8 -*-
from ruminelib.api import RuMineApi as api

rq = dict()
rq["threadId"] = "15781"
rq["pagenum"] = None
rq["b64"] = None

rapi = api(request=rq)
print(rapi.get_comments())