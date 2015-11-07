#!/usr/bin/python
""" Find all raspberry pis listening on the network
    by issuing the 'rolecall' command. Writes all
    responses to the file specified by config.IP_LIST_FILE.
"""

import time

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.internet import task

import config


ROLECALL_TIMEOUT_S = 2

responses = []


class RolecallClient(DatagramProtocol):

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
        with open(config.IP_LIST_FILE, 'w') as outfile:
            for r in responses:
                outfile.write(str(r) + '\n')
        print 'Done. Total responses:', len(responses)

lc = task.LoopingCall(end_rolecall)
lc.start(1)

reactor.listenUDP(config.CONTROLLER_PORT, RolecallClient())
reactor.run()
