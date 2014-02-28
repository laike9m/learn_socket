import socket
import sys

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    print('Failed to create socket %s.' % msg)
    sys.exit()
	
print('Socket Created')

host = 'www.google.com.hk'
port = 80
 
try:
    remote_ip = socket.gethostbyname(host)
except socket.gaierror:
    #could not resolve
    print('Hostname could not be resolved. Exiting')
    sys.exit()

print('Ip address of ' + host + ' is ' + remote_ip)

s.connect((remote_ip, port))

print('Socket Connected to ' + host + ' on ip ' + remote_ip)

# Send some data to remote server
message = "GET / HTTP/1.1\r\n\r\n".encode('utf-8')
 
try :
    # Set the whole string
    s.sendall(message)
except socket.error:
    # Send failed
    print('Send failed')
    sys.exit()
 
print('Message send successfully')

# Receive data
reply = s.recv(4096).decode()
print(reply)

s.close()

