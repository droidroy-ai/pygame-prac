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
            self.acceleration.x = -PLAYER_ACCELERATION
        if key[pg.K_RIGHT]:
            self.acceleration.x = PLAYER_ACCELERATION

        # applying friction
        self.acceleration += self.velocity * PLAYER_FRICTION
        self.velocity += self.acceleration
        self.pos += self.velocity + 0.5 * self.acceleration

        # wrapping player around the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.center = self.pos
