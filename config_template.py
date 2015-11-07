# Common config

# Output debug info
DEBUG = True

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

# Port that the controller uses to listen to pi responses.
# Listen on a different port to MCAST - this allows
# testing of sender & listener on the same machine
CONTROLLER_PORT = 5008

# The base address of this network
IP_BASE_ADDR = '192.168.1.'


# --------------------------------------
# Raspberry pi config

# Network interface used by the pi
PI_NET_INTERFACE = 'eth0'

# Location of scripts / config etc.
PI_DEPLOY_DIR = '/home/pi/uozu/3dscan'

# options for the raspistill command
PI_RASPISTILL_OPTIONS = ''

# directory to save photos to
PI_PHOTOS_DIR = '/tmp/3dscan'

# Set to true if you don't have a camera. Useful for testing.
PI_MOCK_CAMERA = False


# --------------------------------------
# Central controller config

# List of all pis currently listening.
# Updated by rolecall.py
IP_LIST_FILE = 'picam_ips.txt'

# Collect photos from all pis and put in a central location.
# Unnecessary if the pis are saving to a network drive.
COLLECT_PHOTOS = True

# Directory to save photos to (during collection)
COLLECT_PHOTOS_DIR = '/tmp/3dscan'
