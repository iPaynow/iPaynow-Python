#!/usr/bin/env python
# -*- coding: utf-8; mode: python; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- vim:fenc=utf-8:ft=python:et:sw=4:ts=4:sts=4


import ipaynow as ips
#import os
import time
import string
import random
import cgi
try:
    from BaseHTTPServer import BaseHTTPRequestHandler
except ImportError:
    from http.server import BaseHTTPRequestHandler



class GetHandler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        data = self.path
        recvStr = str(data)
        if '?' in self.path:
            recvStr = recvStr[2:]
#            print("recv msg was :{}".format(recvStr))
            info = ips.parseFrontNotify(recvStr)
            self.wfile.write(str(info).encode('utf_8'))
        else:
            self.wfile.write("call error.".encode('utf_8'))
        return
if __name__ == '__main__':
    try:
       from http.server import HTTPServer
    except ImportError:
       from BaseHTTPServer import HTTPServer
    server = HTTPServer(('133.130.109.37', 9530), GetHandler)
    print('Starting server, use <Ctrl + F2> to stop')
    server.serve_forever()
