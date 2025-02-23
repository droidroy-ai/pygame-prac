import pygame as pg

from settings import *

vector = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vector(WIDTH / 2, HEIGHT / 2)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

    def update(self):
        self.acceleration = vector(0, 0)
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            self.acceleration.x = -0.2
        if key[pg.K_RIGHT]:
            self.acceleration.x = 0.2

        self.velocity += self.acceleration
        self.pos += self.velocity + 0.5 * self.acceleration

        self.rect.center = self.pos
