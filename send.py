#!/usr/bin/python
"""
Central command script. Tells all pis to take a photo or reboot.
"""

import os
import subprocess
import time

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

import config


command = raw_input("command/photo name: ")


class CommandClient(DatagramProtocol):

    def startProtocol(self):
        self.transport.write(command, (config.MCAST_GRP, config.MCAST_PORT))


def stop_reactor(s):
    reactor.stop()


def send_command():
    # Send the multicast packet then quit. There's probably simpler
    # way to do this.
    reactor.listenUDP(config.CONTROLLER_PORT, CommandClient())
    reactor.callLater(0.5, stop_reactor, "asdf")
    reactor.run()


def get_pi_ips(path):
    ips = []
    with open(config.IP_LIST_FILE) as infile:
        ips.append(config.IP_BASE_ADDR + infile.readline().strip())
    return ips


def copy_all_photos(remote_path, dest):
    """ Copy photos from each pi to a single location """
    # create dest dir if it doesn't exist
    try:
        os.makedirs(dest)
    except os.error:
        pass
    for ip_addr in get_pi_ips(config.IP_LIST_FILE):
        id = ip_addr.split('.')[-1]
        id = int(id)
        photo_path = remote_path + '_%d.jpg' % id
        cmd = 'scp pi@%s:%s %s' % (ip_addr, photo_path, dest)
        subprocess.call(cmd, shell=True)


send_command()

if command != 'reboot' and command != 'rolecall':
    name = command
    if config.COLLECT_PHOTOS:
        local_photos_dir = os.path.join(config.COLLECT_PHOTOS_DIR, name)
        remote_path = os.path.join(config.PI_PHOTOS_DIR, name, name)
        print 'Wait a bit for photo capture to complete...'
        time.sleep(10)
        print 'Copying photos to', local_photos_dir
        copy_all_photos(remote_path, local_photos_dir)
