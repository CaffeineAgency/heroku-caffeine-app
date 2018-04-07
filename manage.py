#s!/usr/bin/env python
from init import wsgi

app = wsgi.main

def start(*args):
    print(*args)
    app()

if __name__ == "__main__":
    start()