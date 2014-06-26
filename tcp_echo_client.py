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
        s.send(data.encode('utf-8'))
        data = s.recv(size)
        print('Received:', data.decode('utf-8'))
    except KeyboardInterrupt:
        s.close()
