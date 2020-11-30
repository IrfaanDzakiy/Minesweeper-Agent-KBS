import pygame

pygame.font.init()
myfont = pygame.font.SysFont('Open Sans', 29)


class Player:
    def __init__(self):
        self.health = 1

    def sub_health(self):
        self.health -= 1

    def get_health(self):
        return self.health


class Stats:
    @staticmethod
    def draw(surface, label, pos):
        textsurface = myfont.render(label, False, (255, 255, 255))
        surface.blit(textsurface, (pos[0], pos[1]))
