#!/usr/bin/python27root

import commands, pygame, os
from time import sleep
'''
pi@raspberrypi /etc/init.d $ ip addr show dev eth0
2: eth0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc pfifo_fast state DOWN qlen 1000
    link/ether b8:27:eb:7f:23:a9 brd ff:ff:ff:ff:ff:ff
pi@raspberrypi /etc/init.d $ ip addr show dev wlan0
3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP qlen 1000
    link/ether 00:1e:e5:ea:b6:e1 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.109/24 brd 192.168.1.255 scope global wlan0

'''

os.environ["SDL_FBDEV"] = "/dev/fb1"
pygame.init()
pygame.mouse.set_visible(0)
pygame.font.init()
screen = pygame.display.set_mode((128, 160))
font = pygame.font.Font(None, 20)

wired = commands.getoutput("ip addr show dev eth0")
wireless = commands.getoutput("ip addr show dev wlan0")
str = "eth0: "

if ('inet' in wired):
  w = wired.split(' ')
  i = w.index('inet')
  str = str + w[i+1] 
else:
  str = str + "dis"

print str + "\n"
text = font.render(str, True, (255,255,255))
text = pygame.transform.rotate(text, 90)
screen.blit(text, (5, 5))

str = "wlan0: "

if ('inet' in wireless):
  w = wireless.split(' ')
  i = w.index('inet')
  str = str + w[i+1]
else:
  str = str + "dis"

print str + "\n"
text = font.render(str, True, (255,255,255))
text = pygame.transform.rotate(text, 90)
screen.blit(text, (25, 5))


pygame.display.update()

sleep(20)
