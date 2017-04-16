import pygame, sys, random
from pygame.locals import *
from layout import Layout
from life import Conway, HighLife
from pen import Pen
from board import Board

pygame.font.init()

def handleEvent(layout, event):
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    layout.update(event)

def main():
    clock = pygame.time.Clock()
    board = Board(100, 100)
    board.randomFill(30)

    conway = Conway(board)
    layout = Layout(board, conway)

    while True: # main game loop
        for event in pygame.event.get():
            handleEvent(layout, event)

        if (not conway.running):
            handleEvent(layout, pygame.event.wait())
        else:
            conway.next()
            layout.update(force = True)
        pygame.display.update()
        clock.tick(10)

main()
