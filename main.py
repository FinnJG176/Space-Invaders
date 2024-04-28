import pygame
import random
from time import *

# from pygame.sprite import _Group, Group
print("launch.app.python")
print("initializing.pygame")

# Initalize Game
pygame.init()
clock = pygame.time.Clock()
fps = 60
screen = pygame.display.set_mode((800, 600))
time_elapsed = 0

# Game Title
pygame.display.set_caption("Space Invaders")

# Game Pieces
spaceshipX = 400
spaceshipY = 500
enemy_num = 15

enemy_state = "alive"
player_state = "alive"
enemy_font = pygame.font.SysFont("Impact", 60)
player_font = pygame.font.SysFont("Zapfino", 36)
player_font2 = pygame.font.SysFont("Comic Sans", 20)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"img/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = 5
    def update(self):
        self.rect.y -= self.speed
        if self.rect.top < -32:
            self.kill()

class Enemy_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"img/bullet.png")
        # Figure out way to change color
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = 5
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"img/ufo-2.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    def update(self):
        self.rect.move_ip(2, 0)
        if self.rect.left >= 800:
            self.rect.right = 0

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"img/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    def update(self):
        keys = pygame.key.get_pressed()
        if self.rect.top > 536: 
            self.rect.top = 536
        if keys[pygame.K_s]:
            self.rect.left -= 2
        if keys[pygame.K_f]:
            self.rect.left += 2
        if keys[pygame.K_e]:
            self.rect.top -= 2
        if keys[pygame.K_d]:
            self.rect.top += 2 
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top< 0:
            self.rect.top = 0
        if self.rect.left > 736:
            self.rect.left = 736

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"img/exp{num}.png")
            img = pygame.transform.scale(img, (100, 100))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0
    def update(self):
        explosion_speed = 4
        self.counter += 1
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

# create groups
spaceship = Player(spaceshipX, spaceshipY)
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()


for j in range(1, enemy_num+1):
    enemyX = random.randint(0, 536)
    enemyY = random.randint(30, 350)
    enemy = Enemy(enemyX, enemyY)
    all_enemies.add(enemy)
    all_sprites.add(enemy)

all_sprites.add(spaceship)

running = True

# Game Loop 
while running:
    dt = clock.tick(fps)
    time_elapsed += dt
    keys = pygame.key.get_pressed()   
    if player_state == 'dead':
        screen.fill((217, 21, 17))
        text = enemy_font.render('Enemy Wins', True, (0,0,0))
        text2 = enemy_font.render('Press esc to exit', True, (0,0,0))
        screen.blit(text, (300, 300))
        screen.blit(text2, (330, 375))
    elif enemy_state == "alive":
        screen.fill((34, 59, 199)) 
    elif enemy_state == "dead":
        screen.fill((69, 237, 100))
        text = player_font.render('You Win!', True, (175, 181, 53))
        text2 = player_font2.render('Press esc to exit', True, (175, 181, 53))
        screen.blit(text, (300, 300))
        screen.blit(text2, (330, 375))
    
    all_sprites.update()
    all_sprites.draw(screen)
    
    explosion_group.draw(screen)
    explosion_group.update()

    if time_elapsed >= 500 and len(all_enemies) > 0:
        chosen_enemy = random.choice(all_enemies.sprites())
        enemybullet = Enemy_Bullet(chosen_enemy.rect.centerx, chosen_enemy.rect.bottom)
        all_sprites.add(enemybullet)
        enemy_bullets.add(enemybullet)
        time_elapsed = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif player_state == "alive":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(spaceship.rect.centerx, spaceship.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

    if player_state == "dead" or enemy_state == "dead":
        if keys[pygame.K_ESCAPE]:
            pygame.quit()

    s_e_collision = pygame.sprite.spritecollide(spaceship, all_enemies, False)
    # print(collision)
    for enemy in s_e_collision:
        explosion = Explosion(spaceship.rect.centerx, spaceship.rect.centery)
        if spaceship in all_sprites:
            # all_sprites.add(explosion)
            explosion_group.add(explosion)
        spaceship.kill()
        all_sprites.remove(spaceship)
        player_state = "dead"
        
    b_e_collision = pygame.sprite.groupcollide(bullets, all_enemies, True, True)
    for enemy in b_e_collision:
        explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
        explosion_group.add(explosion)
    if len(all_enemies) == 0:
        enemy_state = "dead"

    eb_s_collision = pygame.sprite.spritecollide(spaceship, enemy_bullets, True)
    # print(spaceship)
    for enemybullet in eb_s_collision:
        explosion = Explosion(spaceship.rect.centerx, spaceship.rect.centery)
        if spaceship in all_sprites:
            explosion_group.add(explosion)
        spaceship.kill()
        all_sprites.remove(spaceship)
        player_state = "dead"

    pygame.display.update()

    