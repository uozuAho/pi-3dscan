DEBUG = True

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

# The base address of this network
IP_BASE_ADDR = '192.168.1.'

# List of all pis currently listening.
# Updated by rolecall.py
IP_LIST_FILE = 'picam_ips.txt'


class ListenerConfig:
    def __init__(self):
        # self.NET_INTERFACE = 'eth0'
        # self.NET_INTERFACE = 'wlan0'
        self.NET_INTERFACE = 'wlp2s0'
        # self.DEPLOY_DIR = '/3dscan'
        self.DEPLOY_DIR = '/home/pi/uozu/3dscan'
        # options for the raspistill command
        self.RASPISTILL_OPTIONS = ''
        self.PHOTOS_DIR = '/tmp/3dscan'
        # Set to true if you don't have a camera
        self.MOCK_CAMERA = True


class SenderConfig:
    def __init__(self):
        # Collect photos from all pis and put in a central location
        self.COLLECT_PHOTOS = True
        self.PHOTOS_DIR = '/tmp/3dscan'
        # Listen on a different port to MCAST - allows
        # testing of sender & listener on the same machine
        self.PORT_LISTEN = 5008


# Create config objects
sender = SenderConfig()
listener = ListenerConfig()