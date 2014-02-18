import socket
import sys

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
	print('Failed to create socket. Error code: ')

print('Socket Created')
