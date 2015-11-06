DEBUG = True

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007


class ListenerConfig:
    def __init__(self):
        # self.NET_INTERFACE = 'eth0'
        # self.NET_INTERFACE = 'wlan0'
        self.NET_INTERFACE = 'wlp2s0'
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
        self.IP_BASE_ADDR = '192.168.1.'
        self.IP_RANGE_START = 11
        self.IP_RANGE_END = 11
        # Listen on a different port to MCAST - allows
        # testing of sender & listener on the same machine
        self.PORT_LISTEN = 5008


# Create config objects
sender = SenderConfig()
listener = ListenerConfig()