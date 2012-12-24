#!/usr/bin/python
//todo:
//security 
//switch off debugging 
//cope with warnings that each request sets the GPIO direction each time
//change this to a running daemon that accepts commands on a pipe or unix socket or something. that'll make security easier, it will respond more quickly and allow us to clean up the GPIO configuration on exit

import RPi.GPIO as G
import cgi,cgitb
cgitb.enable()
print("<h1>pin changer</h1>")
print("trying to set mode")
G.setmode(G.BOARD)
print("setting 11 and 12 to out")
G.setup(11,G.OUT)
G.setup(12,G.OUT)


i = cgi.FieldStorage()
print(i)

if "f11" in i:
  if i["f11"].value == '1':
    print("11 on")
    G.output(11, True)
  else:
    print("11 off")
    G.output(11, False)

if "f12" in i:
  if i["f12"].value == '1':
    print("12 on")
    G.output(12, True)
  else:
    print("12 off")
    G.output(12, False)

