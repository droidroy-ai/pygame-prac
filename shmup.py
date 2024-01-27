# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>
# Art from Kenney.nl

from typing import Any
import pygame
import random
import os

WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0 )

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

folder_dir = os.path.dirname(__file__)
img_dir = os.path.join(folder_dir, 'img')
snd_dir = os.path.join(folder_dir, 'snd')

font_name = pygame.font.match_font('arial')
def draw_text(surface, text: str, size: int, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_shield_bar(surface, x: int, y: int, pct: int):
    if pct < 0: # no filling outside of the empty bar
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

def draw_lives(surface, x, y, lives, img):
    """"""
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x  + 30 * i
        img_rect.y = y
        surface.blit(img, img_rect)

def spawn_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        # how long to wait in between each time it shoots in ms
        self.shoot_delay = 250 
        # the time we last shot
        self.last_shot = pygame.time.get_ticks()
        # Number of player lives
        self.lives = 3
        self.hidden = False
        # Timer to control how long the player is hidden
        self.hide_timer = pygame.time.get_ticks()
        self.power_level = 1
        # keeping track of when we picked up the power up
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # timeout for power ups
        if self.power_level >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power_level -= 1
            self.power_time = pygame.time.get_ticks()  

        # check to see if it time to unhide if player is hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2 
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        self.power_level += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        # bullets are fired with a delay with self.shoot_delay
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            # number of bullets at a time depends on power level
            if self.power_level == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power_level >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()


    def hide(self):
        """ Temporarily hide the player """
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.type = random.choice(['shield', 'gun'])
        self.image = power_up_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the bottom of the screen
        if self.rect.top > HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        super().__init__()
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        # To control how quickly the explosion animation happens
        self.frame_rate = 30

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# Load all game graphics
background = pygame.image.load(os.path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()
# player sprite
player_img = pygame.image.load(os.path.join(img_dir, 'playerShip1_blue.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
# meteor_img = pygame.image.load(os.path.join(img_dir, 'meteorGrey_med1.png')).convert()
bullet_img = pygame.image.load(os.path.join(img_dir, 'laserRed16.png')).convert()
meteor_images = []
meteor_list = ['meteorGrey_big1.png', 'meteorGrey_big2.png',
               'meteorGrey_med1.png', 'meteorGrey_med2.png',
               'meteorGrey_small1.png', 'meteorGrey_small2.png',
               'meteorGrey_tiny1.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(os.path.join(img_dir, img)).convert())

# explosion sprites for meteors
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
# explosion sprites for player
explosion_anim['player'] = []
for i in range(1, 5):
    filename = f'explosion0{i}.png'
    img = pygame.image.load(os.path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (70, 65))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (30, 28))
    explosion_anim['sm'].append(img_sm)
    img_mid = pygame.transform.scale(img, (140, 130))
    explosion_anim['player'].append(img_mid)

# power up sprites
power_up_images = {}
power_up_images['shield'] = pygame.image.load(os.path.join(img_dir, 'shield_gold.png')).convert()
power_up_images['gun'] = pygame.image.load(os.path.join(img_dir, 'bolt_gold.png')).convert()

# Load all the game sounds
pygame.mixer.music.load(os.path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)

shoot_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'pew.wav'))
shield_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'pow4.wav'))
power_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'pow5.wav'))

explosion_sounds = []
for snd in ['explosion_1.wav', 'explosion_2.wav']:
    explosion_sounds.append(pygame.mixer.Sound(os.path.join(snd_dir, snd)))
player_die_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'player_die.wav'))

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
power_ups = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    spawn_mob()

# scoring related stuff
score = 0 

pygame.mixer.music.play(loops=-1) # plays the background music
# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
    # Update
    all_sprites.update()

    # check to see if a bullet hits a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius # scoring is relative to the radius of the meteor 
        random.choice(explosion_sounds).play()
        explosion = Explosion(hit.rect.center, 'lg')
        all_sprites.add(explosion)
        if random.random() > 0.9:
            power_up = PowerUp(hit.rect.center)
            all_sprites.add(power_up)
            power_ups.add(power_up)
        spawn_mob()

    # check to see if a mob hits the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in  hits:
        player.shield -= hit.radius * 2
        explosion = Explosion(hit.rect.center, 'sm')
        all_sprites.add(explosion)
        spawn_mob()
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            # hiding the player so no visual clash with explosion
            player.hide()
            player.lives -= 1
            player.shield = 100

    # check to see if player hits a powerup
    hits = pygame.sprite.spritecollide(player, power_ups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            shield_sound.play()
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
            power_sound.play()

    # if the player died and the explosion anim has finished playing
    if player.lives == 0 and not death_explosion.alive():
        running = False

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()