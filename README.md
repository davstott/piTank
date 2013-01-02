piTank
======

Code for Dav's Raspberry Pi Tank

So far, it's as simple as it gets, more a proof of the system required to drive a robot chassis about the place whilst taking photos of where its going with a webcam.

This code uses some HTML and Javascript to provide a simple web interface for forward, left, right and stop, which runs in pretty much any browser that supports javascript.  This interface works well on a mobile phone that's connected to the same network as the Pi.

There's a small CGI python script (cgiPipe.py) that takes a command from the HTML and passes it to another python script (controls.py) that runs all the time in the background (rungpio). The commands are passed through a named pipe in the filesystem. 
controls.py is designed to run just as well from an interactive command prompt as it is from the website, and it is quite responsive. 

Input from the webcam is taken care of by another background process (runwebcam) that simply runs 'fswebcam' and causes it to write a jpeg to the web server's document root on an interval, currently two seconds. This is currently CPU intensive with my Logitech C110 webcam in YUYV mode, I expect that to have a maximum update rate of about 2 frames per second, at the cost of potentially lagging the motor controls.

To run this, you need:
- a Raspberry Pi
- something connected to GPIO pins 17 and 18 to indicate their level, I've used an LED and a 680R resistor on each, connected through AdaFruit's excellent [Prototyping Pi Plate](http://www.adafruit.com/products/801). I've also used a simple transistor circuit and the Pi's 5v supply to control TTL inputs on a motor control board. More details on that later.
- a web server on the Pi (I've used Lighttpd because it came to hand and I know how to make it work)
- a network connection to the Pi (I've used a USB wireless ethernet adaptor and configured the Pi to automatically join my local network)
- set up the background python script so that it can write to /dev/mem
- patience


