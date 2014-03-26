#!/usr/bin/env python
# coding:utf-8

"""
A simple echo client
"""

import socket
import sys

host = '108.59.10.235'
port = 29325
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
