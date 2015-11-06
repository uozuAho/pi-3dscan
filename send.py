#!/usr/bin/python
"""
Central command script. Tells all pis to take a photo.
"""

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
    reactor.listenUDP(config.sender.PORT_LISTEN, CommandClient())
    reactor.callLater(0.5, stop_reactor, "asdf")
    reactor.run()


def copy_all_photos(remote_path, dest):
    """ Copy photos from each pi to a single location """
    # create dest dir if it doesn't exist
    try:
        os.makedirs(dest)
    except os.error:
        pass
    for i in range(config.sender.IP_RANGE_START, config.sender.IP_RANGE_END + 1):
        ip_addr = config.sender.IP_BASE_ADDR + str(i)
        photo_path = remote_path + '_%d.jpg' % i
        cmd = 'scp pi@%s:%s %s' % (ip_addr, photo_path, dest)
        subprocess.call(cmd, shell=True)


send_command()

if command != 'reboot' and command != 'rolecall':
    if config.sender.COLLECT_PHOTOS:
        local_photos_dir = os.path.join(config.sender.PHOTOS_DIR, name)
        remote_path = os.path.join(config.listener.PHOTOS_DIR, name, name)
        # wait for pis to take their photos (takes a while)
        time.sleep(10)
        copy_all_photos(remote_path, local_photos_dir)