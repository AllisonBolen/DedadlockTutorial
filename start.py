import pygame
from pygame.locals import *

def main():
    # initialize
    i = pygame.init()
    print(i)
    # font?
    f = pygame.font.init()
    print(f)
    # set up display
    display_width = 800
    display_height = 600
    game_display = pygame.display.set_mode((display_width, display_height))
    # change game name
    pygame.display.set_caption("Our Game")

    # display the console
    while True:
        eventHandler()
        pygame.display.update()


def eventHandler():
    # loop to keep the window open and to get eevents from user
    for event in pygame.event.get():
        # print(event)
        if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)):
            pygame.quit()
            quit()


if __name__ == "__main__": main()
