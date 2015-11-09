from fabric.api import env, settings
from fabric.operations import run, put, sudo

import config

# get hosts
hosts = []
with open(config.IP_LIST_FILE) as infile:
    for line in infile:
        id = line.strip()
        if id != '':
            hosts.append('pi@' + config.IP_BASE_ADDR + id)
env.hosts = hosts


def pi_setup():
    """ Install required libraries etc. """
    # In case the default rpi servers aren't responding, add these lines to /etc/apt/sources.list
    # deb http://mirror.aarnet.edu.au/pub/raspbian/raspbian wheezy main contrib non-free rpi
    # deb-src http://mirror.aarnet.edu.au/pub/raspbian/raspbian wheezy main contrib non-free rpi
    run('sudo apt-get update')
    run('sudo apt-get install -y python-twisted')


def deploy():
    """ Push config.py & listen.py """
    print 'Make sure config.py is correct!'
    run('mkdir -p ' + config.PI_DEPLOY_DIR)
    put('config.py', config.PI_DEPLOY_DIR + '/config.py')
    put('listen.py', config.PI_DEPLOY_DIR)
    run('chmod +x %s/listen.py' % config.PI_DEPLOY_DIR)


def redeploy():
    """ Kill running listeners, push out new code, restart listeners """
    kill_listener()
    deploy()
    start_listener()


def kill_listener():
    """ Kill running listeners """
    with settings(warn_only=True):
        run('killall -q listen.py')


def start_listener():
    """ Start listeners """
    print 'Press CTRL-c once this command starts'
    # TODO: figure out how to return from this. I've tried
    # run(config.PI_DEPLOY_DIR + '/listen.py &', pty=False),
    # which I couldn't even CTRL-c out of (had to kill the listen.py
    # process in another terminal)
    run(config.PI_DEPLOY_DIR + '/listen.py', pty=False)


def reboot():
    """ Reboot """
    # You can also use send.py and send 'reboot' (no quotes).
    # That should be quicker than using fabric.
    run('sudo reboot')


def poweroff():
    """ Turn off """
    run('sudo poweroff')


if __name__ == "__main__":
    print "Hosts from config file:"
    print hosts
