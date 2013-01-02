#!/usr/bin/python
#todo:
#security
#run as fastcgi

import cgi,cgitb
cgitb.enable()

i = cgi.FieldStorage()

if "q" in i:
  if i["q"].value in ['w','a','d','s']:
    with open('/tmp/gpioControlPipe', 'w') as f:
      f.write(i["q"].value + "\n")

