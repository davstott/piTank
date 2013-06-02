import pygame, os, srf02, time, adc
import matplotlib
matplotlib.use('Agg') # set a non-interactive backend for charting
import pylab

def main():
  global pylab
  #LCD dimensions
  width = 128
  height = 160
  lcdDPI = 80

  # intermediate file used to draw the graph
  imageFileName = "/tmp/lcdSonarGraph.png"  

  # set up the range finder
  # ultrasound
  #s = srf02.srf02()
  title = "Pi sonar"
  # IR
  s = adc.adc()
  title = "Pi iRanger"
  

  # set up pygame to use the framebuffer
  os.environ["SDL_FBDEV"] = "/dev/fb1"
  pygame.init()
  pygame.font.init()
  pygame.mouse.set_visible(0)
  screen = pygame.display.set_mode((width, height))
  bigFont = pygame.font.Font(None, 50)
  littleFont = pygame.font.Font(None, 20)

  # set up matplotlib. size is in inches and dpi. 
  # the dimensions are reversed so we can rotate the image through 90 degrees to show it landscape
  myFig = pylab.figure(figsize = (float(height) / lcdDPI, float(width) / lcdDPI), dpi = lcdDPI)
  axes = myFig.add_subplot(111)
  axes.yaxis.set_ticks((0, 30, 60, 90, 120, 150, 180))
  axes.xaxis.set_visible(False)

  valueHistory = []
  timeHistory = []

  for i in range(100):

    # clear the screen
    screen.fill([0, 0, 0])

    # single pings for now, the SRF doesn't need smoothing
    values = s.getValues(1)

    # add the new value to the chart's arrays
    valueHistory.append(values[0]["distance"])
    timeHistory.append(i)
 
    if (i % 8 == 0):
      # update the chart with the newest values. this takes a couple of seconds so we only do it every few pings
      axes.plot(timeHistory, valueHistory, linewidth=1.0, color='red')
      myFig.savefig(imageFileName, dpi=80, bbox_inches = 'tight', format = 'png') 
      chartImg = pygame.image.load(imageFileName)
      chartImg = pygame.transform.rotate(chartImg, 90)
    # otherwise just draw the old image
    screen.blit(chartImg, (0,0))

    # we should probably only draw this label once and only blank the bit of the screen that changes
    # this should be yellow but my LCD's blue and red signals are swapped
    labelText = littleFont.render(title, True, (0, 215, 255, 0))
    labelText = pygame.transform.rotate(labelText, 90)
    labelTextPosition = labelText.get_rect()
    labelTextPosition.centery = 40
    labelTextPosition.centerx = 123
    screen.blit(labelText, labelTextPosition)

    # draw the result to the screen in jumbo text
    rangeText = bigFont.render(str(values[0]["distance"]) + "cm", True, (0, 140, 0, 0))
    rangeText = pygame.transform.rotate(rangeText, 90)
    rangeTextPosition = rangeText.get_rect()
    rangeTextPosition.centery = 75
    rangeTextPosition.centerx = 40
    screen.blit(rangeText, rangeTextPosition)

    # maybe track dirty rectangles? or try double buffering and use .flip()?
    pygame.display.update()

    time.sleep(0.25)

  raw_input('any key?')

  #myImage = pygame.image.load('pi.png')
  #for j in range(0, 720, 10):
  #  rotated = pygame.transform.rotate(myImage, j)
  #  screen.blit(blank, (0,0))
  #  screen.blit(rotated, (0,0))
  #  pygame.display.update()

  pygame.quit()


if __name__ == '__main__':
    main()

