import pygame as pg
import random

from settings import *
from sprites import *


class Game:
    def __init__(self):
        # Intialize game window and other things
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        # resets the game and start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for platform in PLATFORM_LIST:
            p = Platform(*platform)
            self.platforms.add(p)
            self.all_sprites.add(p)
        self.run()

    def run(self):
        # actual game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game loop - update
        self.all_sprites.update()
        # checking collision between player and platform - only if falling
        if self.player.velocity.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.velocity.y = 0

    def events(self):
        # Game loop - event
        for event in pg.event.get():
            # check for closing the window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        # Game loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen_(self):
        pass

    def show_go_screen(self):
        pass


game = Game()
game.show_start_screen_()
while game.running:
    game.new()
    game.show_go_screen()

pg.quit()
