#!/usr/bin/python
"""
Central command script. Tells all pis to take a photo.
"""

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

import config


name = raw_input("command/photo name: ")


class CommandClient(DatagramProtocol):

    def startProtocol(self):
        # Send the command
        self.transport.write(name, (config.MCAST_GRP, config.MCAST_PORT))


def stop_reactor(s):
    reactor.stop()


reactor.listenUDP(config.sender.PORT_LISTEN, CommandClient())
reactor.callLater(0.5, stop_reactor, "asdf")
reactor.run()
