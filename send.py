#!/usr/bin/env python
import argparse
import sys
import socket
import random
import struct

from scapy.all import sendp, send, get_if_list, get_if_hwaddr, bind_layers, get_if_addr
from scapy.all import Packet
from scapy.all import Ether, IP, UDP, TCP
from scapy.fields import *
import readline

def get_if():
    ifs=get_if_list()
    iface=None # "h1-eth0"
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print "Cannot find eth0 interface"
        exit(1)
    return iface


def main():

    if len(sys.argv)<1:
        print 'pass 1 arguments: <destination_port>'
        exit(1)

    s1 = "10.0.1.254"
    addr = socket.gethostbyname(s1)
    iface = get_if()
    print "sending on interface %s to %s on dport: %s" % (iface, str(addr), sys.argv[1])

    pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff');

    pkt = pkt / IP(src=get_if_addr(iface), dst=addr) / TCP(dport=int(sys.argv[1]), sport=1234)

    pkt.show2()
    sendp(pkt, iface=iface, verbose=False)


if __name__ == '__main__':
    main()
