#!/usr/bin/env python
# coding:utf-8

"""
A simple echo client
"""

import socket
import sys

host = '205.147.105.205'
port = 1111
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

while True:
    try:
        data = sys.stdin.readline()
        s.send(data)
        data = s.recv(size)
        print 'Received:', data
    except KeyboardInterrupt:
        s.close()
