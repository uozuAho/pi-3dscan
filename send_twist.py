#!/usr/bin/python
"""
Central command script. Tells all pis to take a photo.
"""

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

import config


class Pi3dScanClient(DatagramProtocol):

    def startProtocol(self):
        self.transport.write('rolecall', (config.MCAST_GRP, config.MCAST_PORT))

    def datagramReceived(self, datagram, address):
        print "Datagram %s received from %s" % (repr(datagram), repr(address))


reactor.listenUDP(5008, Pi3dScanClient())
reactor.run()
