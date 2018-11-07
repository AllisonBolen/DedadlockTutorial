import pygame, os, generator, sys
from pygame.locals import *

def main():
    stateFile = sys.argv[1]
    
    data = {}
    data = loader(data, stateFile[:stateFile.index(".data")])

    white = (255, 255, 255)
    black = (0,0,0)
    i = pygame.init()
    print(i)
    # font?
    pygame.font.init()
    myfont = pygame.font.SysFont('verdana', 20)
    # set up display
    display_width = 1200
    display_height = 1000
    game_display = pygame.display.set_mode((display_width, display_height))
    # change game name
    pygame.display.set_caption("Our Game")
    game_display.fill(white)

    # display the console
    step = 0
    while True:
        step = step + eventHandler()

        if step > -1 and step < len(data):
            game_display.blit(data[step][0],(300,300))
            #surface = myfont.render(data[step][1], True, black)
            #game_display.blit(surface,(0,1))
            blit_text(game_display, data[step][1], (20, 20), myfont, black)
        if step < 0:
            step = 0
        if step >= len(data):
            step = len(data) - 1

        pygame.display.update()
        blit_text(game_display, data[step][1], (20, 20), myfont, white)

def blit_text(surface, text, pos, font, color):
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
    images_to_read = os.listdir(stateFile+"/images")
    text_to_read = os.listdir(stateFile+"/text")

    for file in range(0,len(images_to_read)):
        data[file]=[]

        for name in images_to_read:
            if int(name[:name.index(".")]) == file:
                imageInfo = stateFile+"/images/"+ name
                image = pygame.image.load(imageInfo)
                data[file].append(image)

        for name in text_to_read:
            if int(name[:name.index(".")]) == file:
                text = stateFile+"/text/"+name
                data[file].append(readText(text))

    return data

def textArray():
    print("here")

def readText(file):
    with open(file) as f:
        content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content]
        content = " ".join(str(x) for x in content)
    print(content)
    return content

def eventHandler():
    # loop to keep the window open and to get eevents from user
    for event in pygame.event.get():
        # print(event)
        if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)):
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                return -1
            if event.key == pygame.K_RIGHT:
                return 1
    return 0
if __name__ == "__main__": main()
