from fabric.api import env
from fabric.operations import run, put

import config

# get hosts
hosts = []
with open(config.IP_LIST_FILE) as infile:
    hosts.append('pi@' + config.IP_BASE_ADDR + infile.readline().strip())
env.hosts = hosts


def test():
    run('echo yo!')


def pi_setup():
    # In case the default rpi servers aren't responding, add these lines to /etc/apt/sources.list
    # deb http://mirror.aarnet.edu.au/pub/raspbian/raspbian wheezy main contrib non-free rpi
    # deb-src http://mirror.aarnet.edu.au/pub/raspbian/raspbian wheezy main contrib non-free rpi
    run('sudo apt-get update')
    run('sudo apt-get install -y python-twisted')


def deploy():
    print 'Make sure config_pi.py is correct!'
    put('config_pi.py', config.listener.DEPLOY_DIR + '/config.py')
    put('listen.py', config.listener.DEPLOY_DIR)
