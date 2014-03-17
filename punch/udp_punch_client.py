#!/usr/bin/env python
# coding:utf-8
# Proof of Concept: UDP Hole Punching
# Two client connect to a server and get redirected to each other.
#
# This is the client.
#
# Koen Bollen <meneer koenbollen nl>
# 2010 GPL
#

import optparse
import sys
import struct
import socket
from threading import Thread, Event

import stun

FullCone = "Full Cone"
RestrictNAT = "Restrict NAT"
RestrictPortNAT = "Restrict Port NAT"
SymmetricNAT = "Symmetric NAT"


def bytes2addr(bytes):
    """Convert a hash to an address pair."""
    if len(bytes) != 6:
        raise ValueError("invalid bytes")
    host = socket.inet_ntoa(bytes[:4])
    port, = struct.unpack("H", bytes[-2:])
    return host, port


class Client():

    def __init__(self):
        try:
            self.master = (sys.argv[1], int(sys.argv[2]))
            self.pool = sys.argv[3].strip()
            self.sockfd = self.target = None
            self.periodic_running = False
        except (IndexError, ValueError):
            print sys.stderr, "usage: %s <host> <port> <pool>" % sys.argv[0]
            sys.exit(65)

    def request_for_connection(self, is_symmetric=False):
        self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockfd.sendto(self.pool, self.master)
        data, addr = self.sockfd.recvfrom(len(self.pool) + 3)
        if data != "ok " + self.pool:
            print sys.stderr, "unable to request!"
            sys.exit(1)
        self.sockfd.sendto("ok", self.master)
        sys.stderr = sys.stdout
        print sys.stderr, "request sent, waiting for partner in pool '%s'..." % self.pool
        data, addr = self.sockfd.recvfrom(6)

        self.target = bytes2addr(data)
        print sys.stderr, "connected to %s:%d" % self.target

    def recv_msg(self, sock, is_restrict=False, event=None):
        if is_restrict:
            while True:
                data, addr = sock.recvfrom(1024)
                if self.periodic_running:
                    print "periodic_send is alive"
                    self.periodic_send = False
                    event.set()
                    print "received msg from target, periodic send cancelled, chat start."
                print(addr)
                if addr == self.target:
                    sys.stdout.write(data)
        else:
            while True:
                data, addr = sock.recvfrom(1024)
                print(addr)
                if addr == self.target:
                    sys.stdout.write(data)

    def send_msg(self, sock):
        while True:
            data = sys.stdin.readline()
            sock.sendto(data, self.target)

    def chat_fullcone(self):
        send_thread = Thread(target=self.send_msg, args=(self.sockfd,))
        send_thread.start()
        recv_thread = Thread(target=self.recv_msg, args=(self.sockfd,))
        recv_thread.start()

    def chat_restrict(self):
        from threading import Timer
        cancel_event = Event()

        def send(count):
            self.sockfd.sendto('torr', self.target)
            print("send torr{0}".format(count))
            if self.periodic_running:
                Timer(0.5, send, args=(count + 1,)).start()

        self.periodic_running = True
        send(0)
        kwargs = {'is_restrict': True, 'event': cancel_event}
        recv_thread = Thread(target=self.recv_msg, args=(self.sockfd,), kwargs=kwargs)
        recv_thread.start()
        cancel_event.wait()
        send_thread = Thread(target=self.send_msg, args=(self.sockfd,))
        send_thread.start()

    def chat_symmetric(self):
        pass

    def main(self, test_nat_type=None):
        if not test_nat_type:
            nat_type, _, _ = self.get_nat_type()
        else:
            nat_type = test_nat_type  # 假装正在测试某种类型的NAT
        if nat_type in (FullCone, RestrictNAT, RestrictPortNAT):
            self.request_for_connection()
            if nat_type == FullCone:
                print("FullCone chat mode")
                self.chat_fullcone()
            else:
                print("Restrict chat mode")
                self.chat_restrict()
        elif nat_type == SymmetricNAT:
            self.request_for_connection(isSymmetric=True)
            self.chat_symmetric()
        else:
            print("NAT type wrong!")

    @staticmethod
    def get_nat_type():
        parser = optparse.OptionParser(version=stun.__version__)
        parser.add_option("-d", "--debug", dest="DEBUG", action="store_true",
                          default=False, help="Enable debug logging")
        parser.add_option("-H", "--host", dest="stun_host", default=None,
                          help="STUN host to use")
        parser.add_option("-P", "--host-port", dest="stun_port", type="int",
                          default=3478, help="STUN host port to use (default: "
                          "3478)")
        parser.add_option("-i", "--interface", dest="source_ip", default="0.0.0.0",
                          help="network interface for client (default: 0.0.0.0)")
        parser.add_option("-p", "--port", dest="source_port", type="int",
                          default=54320, help="port to listen on for client "
                          "(default: 54320)")
        (options, args) = parser.parse_args()
        if options.DEBUG:
            stun.enable_logging()
        kwargs = dict(source_ip=options.source_ip,
                      source_port=int(options.source_port),
                      stun_host=options.stun_host,
                      stun_port=options.stun_port)
        nat_type, external_ip, external_port = stun.get_ip_info(**kwargs)
        print "NAT Type:", nat_type
        print "External IP:", external_ip
        print "External Port:", external_port
        return nat_type, external_ip, external_port

if __name__ == "__main__":
    c = Client()
    #c.main()
    c.main(test_nat_type=RestrictNAT)