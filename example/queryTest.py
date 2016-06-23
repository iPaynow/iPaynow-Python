#!/usr/bin/env python
# -*- coding: utf-8; mode: python; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- vim:fenc=utf-8:ft=python:et:sw=4:ts=4:sts=4


import ipaynow as ips
import time
import string
import random
import cgi
try:
    from BaseHTTPServer import BaseHTTPRequestHandler
except ImportError:
    from http.server import BaseHTTPRequestHandler
try:
    import urllib.request as requestImport
except ImportError:
    import urllib2 as requestImport

def testQueryInterface(orderno = ''):
    paypara = {}
    paypara = {
        'funcode':'MQ001',
        'appId'  :'1409801351286401',
        'mhtCharset': 'UTF-8',
        'mhtSignType':'MD5'
    }
    paypara['mhtOrderNo'] = orderno
    try:
        tradestr = ips.query(paypara)
    except ips.APIInputError as ipse:
        print(ipse)
    except Exception as e:
        print(e)
        print(e.with_traceback)
    return tradestr

def getResponse(URL= "",sendData = "" ,mtd = "POST"):
    #print("getResponse:")
    # method = mtd
    req = requestImport.Request(URL,sendData)
    response = requestImport.urlopen(req)
    recvPage = response.read()
    recvPage = recvPage.decode('utf_8')
    return recvPage

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
        <title>pythonSdk Query Interface</title>
        <head>ipaynow Query interface <head>
        <body>
        <form action="http://133.130.109.37:9528/" METHOD=POST>
        Please input orderno to query:<input type=text name="mhtOrderNo" value=""/><br>
        <button type=submit>submit</button>
        </body>
        </html>
        """.encode('utf_8'))
        return
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
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
        paystr = testQueryInterface(infoDict['mhtOrderNo'])
        recvMsg = getResponse("https://api.ipaynow.cn",paystr.encode('utf_8'),"post")
        recvUnicode = ips.trans2unicode(recvMsg)
        recvGroup = ips.parseQuery(recvUnicode)
        self.wfile.write("The message got was : \n".encode('utf_8'))
        self.wfile.write(recvMsg.encode('utf_8'))
        self.wfile.write("\nParse Result was: \n".encode('utf_8'))
        self.wfile.write(str(recvGroup[0]).encode("utf_8"))
        self.wfile.write("\nMD5 Verified Result:\n".encode('utf_8'))
        self.wfile.write(str(recvGroup[1]).encode("utf_8"))
        ipaynowURL = "https://api.ipaynow.cn/?" + paystr
        self.wfile.write("\nRequest String Was:\n".encode('utf_8'))
        self.wfile.write(ipaynowURL.encode('utf_8'))
        
        return



if __name__ == '__main__':
    try:
        from http.server import HTTPServer
    except ImportError:
        from BaseHTTPServer import HTTPServer 
    server = HTTPServer(('133.130.109.37', 9528), GetHandler)
    print('Starting server, use <Ctrl + F2> to stop')
    server.serve_forever()
