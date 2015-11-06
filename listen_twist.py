#!/usr/bin/python
"""
Shoots photos on request.
"""

import fcntl
import socket
import struct
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

import config


class Pi3dScanServer(DatagramProtocol):

    def startProtocol(self):
        self.transport.joinGroup(config.MCAST_GRP)
        self.setID()
        print "ID: ", self.ID

    def datagramReceived(self, datagram, address):
        if config.DEBUG:
            print "Datagram %s received from %s" % (repr(datagram), repr(address))
        if datagram == "rolecall":
            out_address = (address[0], config.sender.PORT_LISTEN)
            self.transport.write(self.ID, out_address)

    def setID(self):
        addr = get_ip_address(config.listener.NET_INTERFACE)
        ip1, ip2, ip3, ip4 = addr.split('.')
        self.ID = ip4


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915, # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])


reactor.listenMulticast(config.MCAST_PORT, Pi3dScanServer(), listenMultiple=True)
reactor.run()
