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
        # ------------------------------------
        # Network interface that pi listens on
        # self.NET_INTERFACE = 'eth0'
        self.NET_INTERFACE = 'wlan0'
        # self.NET_INTERFACE = 'wlp2s0'

        # ------------------------------------
        # Directory to store scripts & config
        # self.DEPLOY_DIR = '/3dscan'
        self.DEPLOY_DIR = '/home/pi/uozu/3dscan'

        # ------------------------------------
        # options for the raspistill command
        self.RASPISTILL_OPTIONS = ''
        # directory to save photos to
        self.PHOTOS_DIR = '/tmp/3dscan'
        # Set to true if you don't have a camera. Useful for testing.
        self.MOCK_CAMERA = False


class SenderConfig:
    def __init__(self):
        # Collect photos from all pis and put in a central location.
        # Unnecessary if the pis are saving to a network drive.
        self.COLLECT_PHOTOS = False
        # Directory to save photos to (during collection)
        self.PHOTOS_DIR = '/tmp/3dscan'
        # Port to listen to pi responses
        # Listen on a different port to MCAST - allows
        # testing of sender & listener on the same machine
        self.PORT_LISTEN = 5008


# Create config objects
sender = SenderConfig()
listener = ListenerConfig()