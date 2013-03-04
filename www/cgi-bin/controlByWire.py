#!/usr/bin/python
#I've used linux only code for manipulating stdin, but that's ok as it's designed to only run on linux
#Some of this would be less necessary if this script directly opened the pipe in /tmp, instead of listening on stdin, but that makes it harder to work with interactively
#todo: work out why this pegs the cpu 

#todo:
#security

import sys, fcntl, os, select, termios, tty, pygame
#todo: replace with quick2wire's python libraries
import RPi.GPIO as G
from time import sleep
debug = False
usescreen = False

def init():
  if debug:
    print("trying to set mode")
  G.setmode(G.BOARD)
  if debug:
    print("setting 11 and 12 to out and 13 to input with internal pullup active")
  G.setup(11,G.OUT)
  G.setup(12,G.OUT)
  G.setup(13,G.IN, pull_up_down = G.PUD_UP)
  if usescreen:
    if debug:
      print("setting up the fb1 framebuffer")
    os.environ["SDL_FBDEV"] = "/dev/fb1"
    pygame.init()
    pygame.mouse.set_visible(0)
    pygame.font.init()
    screen = pygame.display.set_mode((128, 160))
  else:
    screen = None

  if debug:
    print("Setting stdin to be non blocking and into raw mode instead of line mode")
  fnctlSettings = fcntl.fcntl(sys.stdin.fileno(), fcntl.F_GETFL)
  fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, os.O_NONBLOCK | fnctlSettings)
  termiosSettings = termios.tcgetattr(sys.stdin.fileno())
  tty.setraw(sys.stdin.fileno())
  return [fnctlSettings, termiosSettings, screen]

def sense():
  # is there a byte to be read. if so, read it
  # todo: figure out if it's possible to not block here with less CPU
  sensors = Sensors()
  thisChar = ""

  if (debug):
    print "read?"
  try:
    if select.select([sys.stdin,], [], [], 0)[0]:
      thisChar = sys.stdin.read(1)
    else:
      if (debug):
        print "nothing to read"
  except IOError:
    #nothing to read. should really have checked first
    pass
  
  if (debug):
    print "found: " + thisChar
  # work out which command this byte represents
  if thisChar == "w":  # forward
    sensors.setUserCommand(Commands.FORWARD_full)
  elif thisChar == "f":  # forward slow
    sensors.setUserCommand(Commands.FORWARD_slow)
  elif thisChar == "r":  # forward_medium
    sensors.setUserCommand(Commands.FORWARD_medium)
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

  #using the internal pullup resistor, this assume the switch input connects straight to ground
  sensors.frontBumper = not G.input(13)

  return sensors 

def decide(sensors, cycle, lastCommand):
  if sensors.userCommand == Commands.NONE:
    sensors.userCommand = lastCommand
  if sensors.frontBumper:
    sensors.userCommand = Commands.NONE
    newState = State(Commands.STOP)
  elif sensors.userCommand == Commands.FORWARD_slow:
    if cycle in [3,8]:
      newState = State(Commands.FORWARD_full)
    else:
      newState = State(Commands.STOP)
  elif sensors.userCommand == Commands.FORWARD_medium:
    if cycle in [3,6,9]:
      newState = State(Commands.STOP)
    else:
      newState = State(Commands.FORWARD_full)
  else:
    newState = State(sensors.userCommand)
  return newState

def setMotors(state):
  if state.currentCommand == Commands.FORWARD_full:
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

def updateScreen(screen, state):
  blank = pygame.Surface([128, 160])
  blank.fill([0, 0, 0])
  screen.blit(blank, (0, 0))
  font = pygame.font.Font(None, 30)
  text = font.render('Command: %s' % state.currentCommand, True, (255, 255, 255))
  screen.blit(text, (10, 10))
  pygame.display.update()

class Commands(object):
  NONE, FORWARD_full, LEFT, RIGHT, STOP, QUIT, FORWARD_slow, FORWARD_medium = range(8)

class Sensors(object):
  # todo: add a gpio input for a front bumper switch
  # todo: toString
  userCommand = Commands.NONE
  frontBumper = False
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



originalSettings = init()


#target number of updates per second. hopefully The Loop completes in less time than that.
targetSpeed = 10

# for each trip around This Seems Obvious to Dav AI Loop
# sleep for a bit
# find out if it's time to do anything yet. 
# read next input from sensors
# make any decisions
# set any output

try:
  cycle = 0
  #todo: model state and commands persistently
  lastCommand = Commands.NONE
  while (True):
    # todo: consider using Queue to receive sensor input
    if (debug):
      print str(cycle)
    #todo: keep track of how long the loop takes so we're not assuming infinite cpu speed 
    #todo: look at pygame's tick instead of sleeping
    sleep(1 / targetSpeed)
    if (debug):
      print "slept"
    sensors = sense()
    if (debug):
      print sensors
    thisState = decide(sensors, cycle, lastCommand)
    if (debug):
      print thisState
    setMotors(thisState)
    if usescreen: 
      updateScreen(originalSettings[2], thisState)
    if thisState.currentCommand == Commands.QUIT:
      break;
    if (cycle == 9):
      cycle = 0
    else:
      cycle = cycle + 1
    lastCommand = sensors.userCommand
finally:
  G.cleanup()
  fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, originalSettings[0])
  termios.tcsetattr(sys.stdin.fileno(), termios.TCSAFLUSH, originalSettings[1])

