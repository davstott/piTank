import pygame, os

def main():
  os.environ["SDL_FBDEV"] = "/dev/fb1"
  pygame.init()
  pygame.mouse.set_visible(0)
  screen = pygame.display.set_mode((128, 160))
  blank = pygame.Surface([128, 160])
  blank.fill([0, 0, 0])

  myImage = pygame.image.load('pi.png')
  for j in range(0, 720, 10):
    rotated = pygame.transform.rotate(myImage, j)
    screen.blit(blank, (0,0))
    screen.blit(rotated, (0,0))
    pygame.display.update()

  pygame.quit()


if __name__ == '__main__':
    main()

