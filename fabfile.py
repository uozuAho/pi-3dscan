from fabric.api import env, settings
from fabric.operations import run, put, sudo

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
    print 'Make sure config.py is correct!'
    run('mkdir -p ' + config.listener.DEPLOY_DIR)
    put('config.py', config.listener.DEPLOY_DIR + '/config.py')
    put('listen.py', config.listener.DEPLOY_DIR)
    run('chmod +x %s/listen.py' % config.listener.DEPLOY_DIR)


def redeploy():
    kill_listener()
    deploy()
    start_listener()


def kill_listener():
    with settings(warn_only=True):
        run('killall -q listen.py')


def start_listener():
    print 'Press CTRL-c once this command starts'
    # TODO: figure out how to return from this. I've tried
    # run(config.listener.DEPLOY_DIR + '/listen.py &', pty=False),
    # which I couldn't even CTRL-c out of (had to kill the listen.py
    # process in another terminal)
    run(config.listener.DEPLOY_DIR + '/listen.py', pty=False)


def reboot():
    # You can also use send.py and send 'reboot' (no quotes).
    # That should be quicker than using fabric.
    run('sudo reboot')
