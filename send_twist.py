#!/usr/bin/python
"""
Central command script. Tells all pis to take a photo.
"""

import time

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.internet import task

import config


ROLECALL_TIMEOUT_S = 2

responses = []


class Pi3dScanClient(DatagramProtocol):

    def startProtocol(self):
        self.transport.write('rolecall', (config.MCAST_GRP, config.MCAST_PORT))

    def datagramReceived(self, datagram, address):
        if config.DEBUG:
            print "Datagram %s received from %s" % (repr(datagram), repr(address))
        responses.append(int(datagram))


# Set up a timed task to stop the reactor after the timeout
time_start = time.time()

def end_rolecall():
    if (time.time() - time_start) > ROLECALL_TIMEOUT_S:
        reactor.stop()
        print 'Got responses from:'
        print responses

lc = task.LoopingCall(end_rolecall)
lc.start(1)

reactor.listenUDP(config.sender.PORT_LISTEN, Pi3dScanClient())
reactor.run()
