#!/usr/bin/python
"""
Shoots photos on request.
"""

import socket
import struct
import fcntl
import os
import subprocess
import sys

import config


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', config.MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(config.MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915, # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

id = get_ip_address(config.listener.NET_INTERFACE)

ip1, ip2, ip3, ip4 = id.split('.')

print 'ID: ' + ip4
if config.listener.MOCK_CAMERA:
    print "MOCK_CAMERA is True! Only dummy image files will be generated"
else:
    print "raspistill optons: " + config.listener.RASPISTILL_OPTIONS

def take_photo(dest, options):
    cmd = 'raspistill -o %s %s' % (dest, options)
    pid = subprocess.call(cmd, shell=True)

def photo_path(dir, name, suffix):
    """ Convert a photo name to a path
        Eg. dir/name_suffix.jpg
    """
    filename = name + "_" + suffix + '.jpg'
    return os.path.join(dir, filename)

while True:
    data = sock.recv(10240)
    data = data.strip()
    if data == "reboot":
        print "rebooting..."
        cmd = 'sudo reboot'
        pid = subprocess.call(cmd, shell=True)
    else:
        name = data
        photo_dir = config.listener.PHOTOS_DIR + '/' + name
        try:
            os.makedirs(photo_dir)
        except os.error as e:
            print "Ignoring os.error: ", e
        path = photo_path(photo_dir, name, ip4)
        print "shooting " + name
        if config.listener.MOCK_CAMERA:
            with open(path, 'w') as outfile:
                outfile.write('mock camera. no image!')
        else:
            take_photo(path, config.listener.RASPISTILL_OPTIONS)
