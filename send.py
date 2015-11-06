#!/usr/bin/python
"""
Central command script. Tells all pis to take a photo.
"""

import os
import socket
import subprocess
import sys
import time

IP_BASE_ADDR = '192.168.1.'
IP_RANGE_START = 11
IP_RANGE_END = 11

print 'photo name:'
name = sys.stdin.readline()
name = name.strip('\n')

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007


def initiate_shoot():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    sock.sendto(name, (MCAST_GRP, MCAST_PORT))


def copy_all_photos(remote_path, dest):
    """ Copy photos from each pi to a single location """
    # create dest dir if it doesn't exist
    try:
        os.makedirs(dest)
    except os.error:
        pass
    for i in range(IP_RANGE_START, IP_RANGE_END + 1):
        ip_addr = IP_BASE_ADDR + str(i)
        photo_path = remote_path + '_%d.jpg' % i
        cmd = 'scp pi@%s:%s %s' % (ip_addr, photo_path, dest)
        subprocess.call(cmd, shell=True)


local_photos_dir = '/tmp/3dscan/' + name
remote_path = '/tmp/3dscan/%s/%s' % (name, name)

# shoot
initiate_shoot()
# wait for pis to take their photos (takes a while)
time.sleep(10)
copy_all_photos(remote_path, local_photos_dir)
