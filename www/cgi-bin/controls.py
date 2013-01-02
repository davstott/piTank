#!/usr/bin/python
#todo:
#security

import RPi.GPIO as G
print("trying to set mode")
G.setmode(G.BOARD)
print("setting 11 and 12 to out")
G.setup(11,G.OUT)
G.setup(12,G.OUT)

while (True):
  # this could usefully not require an end of line character
  key = raw_input("w, a, d, s to steer, anything to quit ") 
  if key == "w":  # forward
    G.output(11, True)
    G.output(12, True)
  elif key == "a":  # left
    G.output(11, True)
    G.output(12, False)
  elif key == "d": # right
    G.output(11, False)
    G.output(12, True)
  elif key == "s": # stop
    G.output(11, False)
    G.output(12, False)
  else: # stop and quit program
    G.output(11, False)
    G.output(12, False)
    break

G.cleanup()
