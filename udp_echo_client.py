#!/usr/bin/env python
# coding:utf-8

"""
A simple echo client
"""

import socket
import sys

host = '205.147.105.205'
port = 1112
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


while True:
    try:
        data = sys.stdin.readline()
        s.sendto(data, (host, port))
        data = s.recvfrom(size)
        print('Received:', data.decode('utf-8'))
    except KeyboardInterrupt:
        s.close()
