Multiple Raspberry Pi 3D scanner
--------------------------------

Original project found on [Instructables](http://www.instructables.com/id/Multiple-Raspberry-PI-3D-Scanner/?ALLSTEPS).

# Hardware
- raspberry pi, model 1 (2 probably works), as many as you need
- raspberry pi camera module (1 per pi)
- ethernet hub + many ethernet cables! (1 per pi)

# Software
- python scripts all tested using python 2

## Dependencies
- [fabric](http://www.fabfile.org/) used for some pi task management
- [twisted](https://twistedmatrix.com/trac/) used for networking
    + twisted isn't installed by default on the pi. You can install it
      using fabric: `fab pi_setup` (not the only way, of course...)

# TODO:
- Speed up taking a picture. Currently takes about 7 seconds - maybe use
  the picamera python module to directly interface with the camera in the listen
  script.
