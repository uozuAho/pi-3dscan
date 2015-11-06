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

# --------------------------------------------------------
# Config

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
# NET_INTERFACE = 'eth0'
NET_INTERFACE = 'wlan0'
# options for the raspistill command
RASPISTILL_OPTIONS_PATH = None
PHOTOS_DIR = '/tmp/3dscan'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915, # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

id = get_ip_address(NET_INTERFACE)

ip1, ip2, ip3, ip4 = id.split('.')

print 'ID: ' + ip4

raspistill_options = ''
if RASPISTILL_OPTIONS_PATH is not None:
    with open(RASPISTILL_OPTIONS_PATH) as optionfile:
        raspistill_options = optionfile.readline()
print "raspistill optons: " + raspistill_options

while True:
    data = sock.recv(10240)
    data = data.strip()
    if data == "reboot":
        print "rebooting..."
        cmd = 'sudo reboot'
        pid = subprocess.call(cmd, shell=True)
    else:
        name = data
        print "shooting " + name
        cmd = 'raspistill -o /tmp/photo.jpg ' + raspistill_options
        pid = subprocess.call(cmd, shell=True)
        photo_dir = PHOTOS_DIR + '/' + name
        try:
            os.makedirs(photo_dir)
        except os.error:
            pass
        photo_name = name + "_" + ip4 + '.jpg'
        photo_path = photo_dir + '/' + photo_name
        cmd = 'cp /tmp/photo.jpg ' + photo_path
        pid = subprocess.call(cmd, shell=True)
        print "photo copied to " + photo_path
