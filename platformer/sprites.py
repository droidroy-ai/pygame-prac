import pygame as pg

from settings import *

vector = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game_instance):
        super().__init__()
        self.game = game_instance
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vector(WIDTH / 2, HEIGHT / 2)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

    def jump(self):
        print("JUMP!")
        # jump only when standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.velocity.y = -20

    def update(self):
        self.acceleration = vector(0, PLAYER_GRAVITY)
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            self.acceleration.x = -PLAYER_ACCELERATION
        if key[pg.K_RIGHT]:
            self.acceleration.x = PLAYER_ACCELERATION

        # applying friction
        self.acceleration.x += self.velocity.x * PLAYER_FRICTION
        # eqs of motion
        self.velocity += self.acceleration
        self.pos += self.velocity + 0.5 * self.acceleration

        # wrapping player around the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
