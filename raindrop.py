import pygame
from pygame.sprite import Sprite

class Raindrop(Sprite):
    def __init__(self, engine):
        super().__init__()
        self.screen = engine.screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load('drop_small.png')
        self.rect = self.image.get_rect()
        self.rect.midtop = self.screen_rect.midtop
        self.speed = 1

    def update(self):
        self.rect.y += self.speed
