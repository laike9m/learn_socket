#!/usr/bin/env python
# coding:utf-8

"""
A simple echo client
"""

import socket
import sys

host = '2405:3700:400:202:2:1:0:1f'
port = 29325
size = 1024
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s.connect((host, port))

while True:
    try:
        data = sys.stdin.readline()
        s.send(data)
        data = s.recv(size)
        print 'Received:', data
    except KeyboardInterrupt:
        s.close()
