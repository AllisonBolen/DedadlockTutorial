import pygame, os, generator, sys, shutil
from pygame.locals import *

def main():
    '''
    This is the gui file for the deadlock graphs
    '''
    stateFile = sys.argv[1]
    directory = stateFile[:stateFile.index(".")]+"/"
    # set up the data structure
    # a dict<step#, list<image,text>>
    data = {}
    data = loader(data, stateFile[:stateFile.index(".data")])

    white = (255, 255, 255)
    black = (0,0,0)

    i = pygame.init()
    # font
    pygame.font.init()
    myfont = pygame.font.SysFont('verdana', 20)
    # set up display
    display_width = 1200
    display_height = 1000
    game_display = pygame.display.set_mode((display_width, display_height))
    # change game name
    pygame.display.set_caption("Our Game")
    game_display.fill(white)

    step = 0
    while True:
        # catch user events and update the step
        # counter to present the right step
        step = step + eventHandler(directory)
        if step > -1 and step < len(data):
            game_display.blit(data[step][0],(300,300))
            blit_text(game_display, data[step][1], (20, 20), myfont, black)
        if step < 0:
            # bounds guard
            step = 0
        if step >= len(data):
            # bounds guard
            step = len(data) - 1

        pygame.display.update()
        # "erase" the text from the window
        blit_text(game_display, data[step][1], (20, 20), myfont, white)

def blit_text(surface, text, pos, font, color):
    '''
    https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame
    Organize text in the window
    '''
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

def loader(data, stateFile):
    '''
    Loads the files for the gui to present
    '''
    images_to_read = os.listdir(stateFile+"/images")
    text_to_read = os.listdir(stateFile+"/text")

    for file in range(0,len(images_to_read)):
        data[file]=[]

        for name in images_to_read:
            if int(name[:name.index(".")]) == file:
                # add the image to the dict to load
                imageInfo = stateFile+"/images/"+ name
                image = pygame.image.load(imageInfo)
                data[file].append(image)

        for name in text_to_read:
            if int(name[:name.index(".")]) == file:
                # add text to the step in the dict to load
                text = stateFile+"/text/"+name
                data[file].append(readText(text))

    return data

def cleanUp(dir):
    if os.path.isdir(dir) is True:
        shutil.rmtree(dir)

def readText(file):
    '''
    Read the text from the file to be presented on screen
    '''
    with open(file) as f:
        content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content]
        content = " ".join(str(x) for x in content)

    return content

def eventHandler(directory):
    '''
    Detect events from the user
    '''
    # loop to keep the window open and to get events from user
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)):
            cleanUp(directory)
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # go to the previous step
                return -1
            if event.key == pygame.K_RIGHT:
                # go to the next step
                return 1
    return 0

if __name__ == "__main__": main()
