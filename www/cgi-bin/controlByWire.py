#!/usr/bin/python
#todo:
#security
#non-scalar data types 

import sys
import RPi.GPIO as G
from time import sleep
#todo: look at pygame's tick instead of sleeping

def init():
  print("trying to set mode")
  G.setmode(G.BOARD)
  print("setting 11 and 12 to out")
  G.setup(11,G.OUT)
  G.setup(12,G.OUT)

def sense():
  # is there a byte to be read. if so, read it
  # todo: figure out if it's possible to not block here. another thread? Queue? 
  # also, no carriage returns
  if (debug):
    print "read?"
  thisChar = sys.stdin.read(1)
  if (debug):
    print "found: " + thisChar
  sensors = Sensors()
  # work out which command this byte represents
  if thisChar == "w":  # forward
    sensors.setUserCommand(Commands.FORWARD)
  elif thisChar == "a":  # left
    sensors.setUserCommand(Commands.LEFT)
  elif thisChar == "d": # right
    sensors.setUserCommand(Commands.RIGHT)
  elif thisChar == "s": # stop
    sensors.setUserCommand(Commands.STOP)
  elif thisChar == "q": # quit
    sensors.setUserCommand(Commands.QUIT)
  else: # no command received
    sensors.setUserCommand(Commands.NONE)
  #todo: add a class for other sensors and package up the return from this function
  return sensors 

def decide(sensors):
  #todo: this
  newState = State(sensors.userCommand)
  return newState

def setMotors(state):
  if state.currentCommand == Commands.FORWARD:
    G.output(11, True)
    G.output(12, True)
  elif state.currentCommand == Commands.LEFT:
    G.output(11, True)
    G.output(12, False)
  elif state.currentCommand == Commands.RIGHT:
    G.output(11, False)
    G.output(12, True)
  elif state.currentCommand == Commands.STOP:
    G.output(11, False)
    G.output(12, False)
  elif state.currentCommand == Commands.QUIT:
    G.output(11, False)
    G.output(12, False)


class Commands(object):
  NONE, FORWARD, LEFT, RIGHT, STOP, QUIT = range(6)

class Sensors(object):
  # todo: add a gpio input for a front bumper switch
  # todo: toString
  userCommand = Commands.NONE
  def setUserCommand(self, command):
    self.userCommand = command

class State(object):
  #todo: change this to having a current state and next state which generates a collection of commands
  #to get from one to the next?
  #todo: tostring
  currentCommand = Commands.NONE
  def __init__(self, startCommand):
    if startCommand == None:
      self.currentCommand = Commands.STOP
    else:
      self.currentCommand = startCommand


debug = False
init()

#target number of updates per second. hopefully The Loop completes in less time than that.
targetSpeed = 10

# for each trip around This Seems Obvious to Dav AI Loop
# sleep for a bit
# find out if it's time to do anything yet. 
# read next input from sensors
# make any decisions
# set any output

while (True):
# todo: consider using Queue to receive sensor input
  if (debug): 
    print "go sleep"
  #todo: keep track of how long the loop takes so we're not assuming infinite cpu speed 
  sleep(1 / targetSpeed)
  if (debug) :
    print "slept"
  sensors = sense() 
  if (debug):
    print sensors
  thisState = decide(sensors)
  if (debug):
    print thisState
  setMotors(thisState)
  if thisState.currentCommand == Commands.QUIT:
    break;


G.cleanup()


