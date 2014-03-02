# -*- coding:utf-8 -*-
"""
这个服务器会把HTTP请求的头部给加入html里面返回
"""
import asyncore
import asynchat
import socket

PORT = 8000


class HTTPChannel(asynchat.async_chat):

    def __init__(self, server, sock, addr):
        asynchat.async_chat.__init__(self, sock)
        self.set_terminator("\r\n")
        self.request = None
        self.data = ""
        self.shutdown = 0

    def collect_incoming_data(self, data):
        print data
        self.data += data   # 每次接收到的data是否包含/r/n？

    def found_terminator(self):
        if not self.request:
            # got the request line: GET / HTTP/1.1
            print "request: ", self.request
            print "data: ", self.data
            self.request = self.data.split(None, 2)  # return [] if data is None
            print self.request
            if len(self.request) != 3:
                self.shutdown = 1
            else:
                self.push("HTTP/1.0 200 OK\r\n")
                self.push("Content-type: text/html\r\n")
                self.push("\r\n")
            self.data += "\r\n"  # terminator is swallowed, add it manually
            self.set_terminator("\r\n\r\n")  # look for end of headers
        else:
            # return payload.
            self.push("<html><body><pre>\r\n")
            self.push(self.data)
            self.push("</pre></body></html>\r\n")
            self.close_when_done()


class HTTPServer(asyncore.dispatcher):

    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(("", port))
        self.listen(5)

    def handle_accept(self):
        conn, addr = self.accept()
        HTTPChannel(self, conn, addr)


s = HTTPServer(PORT)
print "serving at port", PORT, "..."
asyncore.loop()
