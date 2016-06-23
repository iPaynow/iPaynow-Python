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
except ImportError as e:
#    print(e)
    from http.server import BaseHTTPRequestHandler

def testTradeInterface(amt = 1, orderno = '',ordername = 'ordername'):
    #
    paypara = {}
    paypara = {
        'funcode':'WP001',
        'appId'  :'1409801351286401',
        'mhtOrderType' :'01',
        'mhtCurrencyType':'156',
        'mhtOrderDetail':'ipaynowPythonSDKTestOrder',
        'mhtOrderTimeOut':120,
        'notifyUrl':'http://133.130.109.37:9529/',
        'frontNotifyUrl':'http://133.130.109.37:9530/',
        'mhtCharset': 'UTF-8',
        'deviceType': '02',
        'payChannelType' : '',
        'mhtReserved':'',
        'consumerId':'',
        'consumerName':'',
        'mhtSignType':'MD5'
    }
    timestr = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    if len(orderno) == 0:
        orderno = timestr + '_' +''.join(random.sample(string.ascii_letters, 16))
    paypara['mhtOrderStartTime'] = timestr
    paypara['mhtOrderNo'] = orderno
    paypara['mhtOrderName'] = ordername
    paypara['mhtOrderAmt'] = amt
    try:
        tradestr = ips.trade(paypara)
    except ips.APIInputError as ipse:
        print(ipse)
    except Exception as e:
        print(e)
        print(e.with_traceback)
    return tradestr

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
        <title>pyonSdktest</title>
        <head>ipaynowPythonSdkTest</head>
        <body>
        <form action="http://133.130.109.37:9527/" METHOD=POST>
        OrderName:<input type=text name="mhtOrderName" value="PythonSdkTestOrder"/><br>
        Amt      :<input type=text name="mhtOrderAmt" value="10"/><br>
        Desp     :<input type=text name="mhtOrderDetail" value="PoweredByIpaynow"/><br>
        <button type=submit>sumit</button>
        </body>
        </html>
        """.encode('utf_8'))
        return
    def do_POST(self):
        self.send_response(302)
        # Parse the form data posted
        form = cgi.FieldStorage(
        fp=self.rfile,
        headers=self.headers,
        environ={'REQUEST_METHOD':'POST',
          'CONTENT_TYPE':self.headers['Content-Type'],
        })
         # Begin the response
        infoDict = {}
        for field in form.keys():
            infoDict[field] = form[field].value
        print(infoDict['mhtOrderAmt'])
        paystr = testTradeInterface(infoDict['mhtOrderAmt'])
        ipaynowURL = """https://api.ipaynow.cn/?""" + paystr
#        print(ipaynowURL)
#        self.wfile.write(ipaynowURL.encode('utf_8'))
        self.send_header(keyword='Location',value=ipaynowURL)
        self.end_headers()
        return


if __name__ == '__main__':

    try:
       from http.server import HTTPServer
    except ImportError:
       from BaseHTTPServer import HTTPServer
    server = HTTPServer(('133.130.109.37', 9527), GetHandler)
    print('Starting server, use <Ctrl + F2> to stop')
    server.serve_forever()
