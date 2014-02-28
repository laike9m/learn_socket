import socket
import sys

from threading import Thread
 
HOST = ''    # Symbolic name meaning all available interfaces
PORT = 8887  # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
 
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed %s.' % msg)
    sys.exit()
     
print('Socket bind complete')

s.listen(10)
print('Socket now listening')

# now keep talking with the client
def client_thread(conn):
    while True:
        conn.send('Welcome to the server. Type something and hit enter\n'.encode('utf-8'))

        # wait to accept a connection - blocking call
        data = conn.recv(1024).decode('utf-8')
        reply = 'OK...' + data
        if not data:
            break
 
        conn.sendall(reply.encode('utf-8'))
    conn.close()


while True:
    # wait to accept a connection - blocking call
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
     
    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    new_conn = Thread(target=client_thread ,args=(conn,))
    new_conn.start()

s.close()
