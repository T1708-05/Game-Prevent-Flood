import pygame
from login_startgame import *

# constant
WIDTH, HEIGHT, FPS = 1300, 750, 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Prevent floods Game ")

def getImage(filename: str):
    return pygame.image.load(rf'assets\{filename}').convert_alpha()

# main function
def main():
    g = LoginMenu()
    g.start()

if __name__ == '__main__':
    main()