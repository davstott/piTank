#!/usr/bin/python
#todo: 
#security
#use pi's kernel drivers instead of RPi.gpio

from flup.server.fcgi import WSGIServer
import sys, urlparse

def app(environ, start_response):
  start_response("200 OK", [("Content-Type", "text/html")])
  i = urlparse.parse_qs(environ["QUERY_STRING"])
# useful because flup is expecting a string to be returned
  yield ('&nbsp;') 
  if "q" in i:
    if i["q"][0] in ['w','a','d','s']:
      with open('/tmp/gpioControlPipe', 'w') as f:
        f.write(i["q"][0] + "\n")

WSGIServer(app).run()
