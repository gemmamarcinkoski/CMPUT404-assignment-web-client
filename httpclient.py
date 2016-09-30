#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
import urllib

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):
        #splitting host, port, and path from extras
        parse = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*?(?P<path>[^?#]*)(?P<extras>\?([^#]*))'
        match = re.search(parse, url)
        
        self.host = match.group('host')
        print "host: ", self.host
        
        self.port = match.group('port')
        print "port: ", self.port
        
        self.path = match.group('path')
        extras = match.group('extras')
        
        if self.path:
            self.path = "/" + self.path
        if extras:
            self.path += extras
        if not self.port:
            self.port = 80
        

    def connect(self, url):
        #connecting socket
        #CALLING GET HOST PORT HERE
        self.get_host_port(url)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, int(self.port)))
        return sock
    
    def make_headers(self,method,path, data=None):
        print method, path
        header = "%s %s HTTP/1.1\r\n" % (method, path) \
            + "Host: %s\r\n" % (self.host)\
            + "Connection: Keep-Alive\r\n"
        # header lines for post
        if data:
            content - urllib.urlencode(data)
            header += "Content-Length: %d\r\n" %(len(content)) \
                + "\r\n" + content + "\r\n"
        return header + "\n"

    def get_code(self, data):
        # getting HTTP response code
        print "GET CODE: ", int(data.split(' ')[1])
        return int(data.split('')[1])

    def get_body(self, data):
        return data.split("\r\n\r\n", 1)[1]

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        # CALLING CONNECT IN HERE
        # CALLING MAKE HEADERS IN HERE
        # CALLINF GET CODE AND GET BODY IN HERE
        code = 500
        body = ""
        print "HERE I AM GETTING", url
        connection = self.connect(url)
        request = self.make_headers('GET', self.path)
        print "REQUEST: ", request
        connection.sendall(request)
        
        response = self.recvall(connection)
        print response
        code = self.get_code(response)
        body = self.get_body(response)
        print code, "BODY", body
        
        connection.close()
        return HTTPRequest(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        
        connection = self.connect(url)
        request = self.make_headers('POST', self.path, args)
        
        connection.sendall(request)
        response = self.recvall(connection)
        split = response.split(' ')[1]
        
        code = self.get_code(response)
        print code
        body = self.get_body(response)
        
        connection.close()
        
        return HTTPRequest(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
   
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )   
