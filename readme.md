Multiple Raspberry Pi 3D scanner
--------------------------------

Original project found on [Instructables](http://www.instructables.com/id/Multiple-Raspberry-PI-3D-Scanner/?ALLSTEPS).

# Hardware
- raspberry pi, model 1 (2 probably works), as many as you need
- raspberry pi camera module (1 per pi)
- ethernet switch/router + many ethernet cables! (1 per pi)

# Software
- python scripts all tested using python 2

## Dependencies
- [fabric](http://www.fabfile.org/) used for pi management
- [twisted](https://twistedmatrix.com/trac/) used for networking
    + twisted isn't installed by default on the pi. You can install it
      on all pis using fabric: `fab pi_setup`. This requires the pi to be
      connected to the internet.

# Usage
**Assumed setup**
- All pis have a camera attached & enabled, are connected to a network and
  are turned on
- All pis have twisted installed
- A 'central command' computer to run scripts is also connected to the same
  network

**Steps**
- Get the IP addresses of all pis, put the last number of each into a file
  in this directory called picam_ips.txt (one number per line). Eg. If a pi
  has the address 192.168.1.7, put 7 in the file. This process can be automated
  once all pis are running the listen script.
  I guess you could just put the numbers 1-255 in picam_ips.txt to be sure
  that all pis are accounted for.
- Copy config_template.py to config.py, modify it to suit your requirements
- Run `fab deploy` on the central command computer. This will copy necessary
  files to all connected pis.
- Run `fab start_listener` to tell all pis to start listening for commands.
  You have to ctrl-c out of this, since I don't know how to start a background
  process with fabric yet :(. This should still leave listen.py running on the
  pis.
- Run `./rolecall.py` to check which pis are running listen.py. Note that this
  will overwrite picam_ips.txt.
- Run `./send.py`, enter a name for a photo. All pis should take a photo at
  this point. If you've configured them to save to a network location, photos
  should start appearing there. Otherwise, the central computer will start
  collecting photos from all the pis.
- If you update config.py or listen.py, run `fab redeploy` to push out the
  changes and restart the listener on all pis.


# TODO:
- Fix fab start_listener. Currently need to ctrl-c out of it.
- Speed up taking a picture. Currently takes about 7 seconds - maybe use
  the picamera python module to directly interface with the camera in the listen
  script.
