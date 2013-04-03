piTank
======

Code for Dav's Raspberry Pi Tank

So far, it's as simple as it gets, more a proof of the system required to drive a robot chassis about the place whilst taking photos of where its going with a webcam.

This code uses some HTML and Javascript to provide a simple web interface for forward, left, right and stop, which runs in pretty much any browser that supports javascript.  This interface works well on a mobile phone that's connected to the same network as the Pi.

There's a small FastCGI python script (fcgiPipe.py) that takes a command from the HTML and passes it to another python script (controls.py) that runs all the time in the background (rungpio). The commands are passed through a named pipe in the filesystem. 
controls.py is designed to run just as well from an interactive command prompt as it is from the website, and it is quite responsive. 

For variable speeds, there is controlByWire.py which runs some extremely crude PWM for different ahead speeds. It also has an input for a front bumper switch for emergency stops.

LCD support is in! It assumes that /dev/fb1 is connected up to an ST7735R LCD (details here: http://marks-space.com/2012/11/23/raspberrypi-tft/)
However, be careful because updating the LCD using pygame is relatively slow and ruins my crude PWM

Input from the webcam is taken care of by another background process (runwebcam) that simply runs 'fswebcam' and causes it to write a jpeg to the web server's document root on an interval, currently two seconds. This is currently CPU intensive with my Logitech C110 webcam in YUYV mode, I expect that to have a maximum update rate of about 2 frames per second, at the cost of potentially lagging the motor controls.

To run this, you need:
- a Raspberry Pi
- something connected to GPIO pins 17 and 18 to indicate their level, I've used an LED and a 680R resistor on each, connected through AdaFruit's excellent [Prototyping Pi Plate](http://www.adafruit.com/products/801). I've also used a simple transistor circuit and the Pi's 5v supply to control TTL inputs on a motor control board. More details on that later.
- a switch connected to GPIO pin 21 that connects to ground, to act as a front bumper emergency stop
- a web server on the Pi (I've used Lighttpd because it came to hand and I know how to make it work)
- a network connection to the Pi (I've used a USB wireless ethernet adaptor and configured the Pi to automatically join my local network)
- set up the background python script so that it can write to /dev/mem
- patience

Configuring your web server
===========================

CGI
===


The simplest configuration is CGI. This spawns a new python process for every http request which is simple to set up but adds a lot to the system load and adds up to a second of lag in the controls, which isn't ideal.

My lighttpd fragment for cgi looks like this:

> server.modules = (
>   <some modules>,
>    "mod_cgi"
> )
> 
> $HTTP["url"] =~ "^/cgi-bin/" {
>         cgi.assign = ( ".py" => "/usr/bin/python" )
> }

FastCGI
=======

FastCGI is a bit old style for hooking up Python scripts to a HTTP request, but it's still hugely better than CGI because it leaves a process running all the time on the server so it responds almost immediately. One of the downsides is that you have to structure your application code slightly differently, you can't have different .py files directly hooked up to the web server, yo uneed to have a single entry point for your application. Which admittedly could just include() the necessary .py file based on the cgi.script_name parameter.

You also need a non default Python library called Flup which deals with gluing your script to the server.

> apt-get -no-install-recommended install python-flup

My lighttpd configuration for FastCGI looks like this:

> fastcgi.server = (
>   ".py" => (
>     "python-fcgi" => (
>       "socket" => "/tmp/fastcgi.python.socket",
>       "bin-path" => "/var/www/cgi-bin/fcgiPipe.py",
>       "check-local" => "disable",
>       "max-procs" => 1)
>   )
> )

