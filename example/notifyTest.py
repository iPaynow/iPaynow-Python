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
        self.wfile.write("""
        <html>
        <title>现在支付PythonSdk</title>
        <head>商户接收订单通知服务已启动</head>
        <body>
        </body>
        </html>
        """.encode('utf_8'))
        return
    def do_POST(self):
        self.send_response(200)
        self.end_headers()        
        data = self.rfile.read(int(self.headers['content-length']))
        recvStr = str(data,encoding = 'utf8')
        print("recv msg was :{}".format(recvStr))
        print("Start Parse Info:")
        infoDict = ips.parseNotify(recvStr)
        print(str(infoDict))
        strRtn = ips.notify('Y')
        print(strRtn)
        self.wfile.write(strRtn.encode('utf_8'))
        return



if __name__ == '__main__':
    try:
       from http.server import HTTPServer
    except ImportError:
       from BaseHTTPServer import HTTPServer
    server = HTTPServer(('133.130.109.37', 9529), GetHandler)
    print('Starting server, use <Ctrl + F2> to stop')
    server.serve_forever()
