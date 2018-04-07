#s!/usr/bin/env python
from init import wsgi

app = wsgi.main

def start():
    app()

if __name__ == "__main__":
    start()