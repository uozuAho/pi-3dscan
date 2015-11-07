#!/usr/bin/python
"""
Shoots photos on request.
"""

import fcntl
import os
import socket
import struct
import subprocess

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

import config


class Pi3dScanServer(DatagramProtocol):

    def startProtocol(self):
        self.transport.joinGroup(config.MCAST_GRP)
        self.setID()
        print "ID: ", self.ID
        if config.PI_MOCK_CAMERA:
            print "PI_MOCK_CAMERA is True! Only dummy image files will be generated"
        else:
            print "raspistill optons: " + config.PI_RASPISTILL_OPTIONS

    def setID(self):
        addr = get_ip_address(config.PI_NET_INTERFACE)
        ip1, ip2, ip3, ip4 = addr.split('.')
        self.ID = ip4

    def datagramReceived(self, datagram, address):
        if config.DEBUG:
            print "Datagram %s received from %s" % (repr(datagram), repr(address))
        if datagram == "reboot":
            print "rebooting..."
            cmd = 'sudo reboot'
            pid = subprocess.call(cmd, shell=True)
        elif datagram == "rolecall":
            out_address = (address[0], config.CONTROLLER_PORT)
            self.transport.write(self.ID, out_address)
        else:
            name = datagram
            photo_dir = config.PI_PHOTOS_DIR + '/' + name
            makedirs(photo_dir)
            path = photo_path(photo_dir, name, self.ID)
            take_photo(path)


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915, # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])


def makedirs(path):
    try:
        os.makedirs(path)
    except os.error as e:
        print "Ignoring os.error: ", e


def take_photo(dest):
    print "capturing " + dest
    if config.PI_MOCK_CAMERA:
        with open(dest, 'w') as outfile:
            outfile.write('mock camera. no image!')
    else:
        cmd = 'raspistill -o %s %s' % (dest, config.PI_RASPISTILL_OPTIONS)
        pid = subprocess.call(cmd, shell=True)
    print 'done.'


def photo_path(dir, name, suffix):
    """ Convert a photo name to a path
        Eg. dir/name_suffix.jpg
    """
    filename = name + "_" + suffix + '.jpg'
    return os.path.join(dir, filename)


reactor.listenMulticast(config.MCAST_PORT, Pi3dScanServer(), listenMultiple=True)
reactor.run()
