#!/usr/bin/python
"""
Shoots photos on request.
"""

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

import config


class Pi3dScanServer(DatagramProtocol):

    def startProtocol(self):
        self.transport.joinGroup(config.MCAST_GRP)

    def datagramReceived(self, datagram, address):
        print "Datagram %s received from %s" % (repr(datagram), repr(address))
        if datagram == "rolecall":
            out_address = (address[0], 5008)
            self.transport.write("hi", out_address)

reactor.listenMulticast(config.MCAST_PORT, Pi3dScanServer(), listenMultiple=True)
reactor.run()
