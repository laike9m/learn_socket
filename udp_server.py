import socket

from threading import Thread
 
HOST = ''    # Symbolic name meaning all available interfaces
PORT = 1112  # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
print('Socket created')


# now keep talking with the client
def client_thread(sock):
    while True:
        # wait to accept a connection - blocking call
        data, addr = sock.recvfrom(1024)
        print('Connected with ' + addr[0] + ':' + str(addr[1]))
        data = data.decode('utf-8')
        reply = 'OK...' + data
        if not data:
            break

        print(data)
        sock.sendto(reply.encode('utf-8'), addr)


def main():
    new_conn = Thread(target=client_thread, args=(s,))
    new_conn.start()


if __name__ == '__main__':
    main()
