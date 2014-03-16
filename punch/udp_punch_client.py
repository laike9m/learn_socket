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
from threading import Thread

import stun


def bytes2addr(bytes):
    """Convert a hash to an address pair."""
    if len(bytes) != 6:
        raise ValueError("invalid bytes")
    host = socket.inet_ntoa(bytes[:4])
    port, = struct.unpack("H", bytes[-2:])
    return host, port


def main():
    get_nat_type()
    try:
        master = (sys.argv[1], int(sys.argv[2]))
        pool = sys.argv[3].strip()
    except (IndexError, ValueError):
        print sys.stderr, "usage: %s <host> <port> <pool>" % sys.argv[0]
        sys.exit(65)

    sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockfd.sendto(pool, master)
    data, addr = sockfd.recvfrom(len(pool)+3)
    if data != "ok " + pool:
        print sys.stderr, "unable to request!"
        sys.exit(1)
    sockfd.sendto("ok", master)
    sys.stderr = sys.stdout
    print sys.stderr, "request sent, waiting for partner in pool '%s'..." % pool
    data, addr = sockfd.recvfrom(6)

    target = bytes2addr(data)
    print sys.stderr, "connected to %s:%d" % target

    sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_msg(sock):
        while True:
            data = sys.stdin.readline()
            sock.sendto(data, target)

    def recv_msg(sock):
        while True:
            data, addr = sock.recvfrom(1024)
            sys.stdout.write(data)

    send_thread = Thread(target=send_msg, args=(sock_send,))
    send_thread.start()
    recv_thread = Thread(target=recv_msg, args=(sockfd,))
    recv_thread.start()


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

if __name__ == "__main__":
    main()