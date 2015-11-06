#!/usr/bin/python
"""
Central command script. Tells all pis to take a photo.
"""

import os
import socket
import subprocess
import sys
import time

import config


print 'photo name:'
name = sys.stdin.readline()
name = name.strip('\n')


def initiate_shoot():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    sock.sendto(name, (config.MCAST_GRP, config.MCAST_PORT))


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


# shoot
initiate_shoot()

if config.sender.COLLECT_PHOTOS:
    local_photos_dir = os.path.join(config.sender.PHOTOS_DIR, name)
    remote_path = '/tmp/3dscan/%s/%s' % (name, name)
    # wait for pis to take their photos (takes a while)
    time.sleep(10)
    copy_all_photos(remote_path, local_photos_dir)
