import pygame
from board import Grid
from player import Player, Stats
from enum import Enum, auto

import os
import sys
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (400, 100)

display_heigth = 1200
display_width = 900
surface = pygame.display.set_mode((display_heigth, display_width))
pygame.display.set_caption('Minesweeper')


class States(Enum):
    running = auto()
    game_over = auto()
    win = auto()


state = States.running
player = Player()
filename = sys.argv[1]

f = open("input.txt", "r")
size = int(f.readline())
row = int(f.readline())
mines = [[False for i in range(size)] for j in range(size)]
for i in range(row):
    res = f.readline()
    i, j = tuple(map(int, res.split(', ')))
    mines[i][j] = True

grid = Grid(player, size, mines)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and state == States.running:
            # check for the left mouse button
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                grid.click(pos[0], pos[1])
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                grid.mark_mine(pos[0], pos[1])
            if grid.check_if_win():
                state = States.win
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and (state == States.game_over or state == States.win):
                grid.reload()
                state = States.running
            if event.key == pygame.K_b:
                grid.show_mines()

    surface.fill((255, 255, 153))

    if player.get_health() == 0:
        state = States.game_over

    pygame.draw.rect(surface, (255, 102, 102),
                     (900, 0, 300, 900))
    if state == States.game_over:
        Stats.draw(surface, 'GAME OVER!', (990, 350))
        Stats.draw(surface, 'PRESS SPACE TO RESTART', (920, 400))
    elif state == States.win:
        Stats.draw(surface, 'YOU WIN!', (1000, 350))
        Stats.draw(surface, 'PRESS SPACE TO RESTART', (920, 400))

    grid.draw(surface)
    Stats.draw(surface, 'RMB TO MARK MINE', (955, 550))
    Stats.draw(surface, 'PRESS B TO SHOW MINES', (925, 650))

    pygame.display.flip()
