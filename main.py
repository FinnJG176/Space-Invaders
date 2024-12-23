import pygame
import random
from time import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Initalize Game
pygame.init()
print("applaunch.git.python.pygame")

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# SCREEN_CENTER = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 30)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YOUWINSF = (69, 237, 100)
YOUWINTC = (175, 181, 53)
YOULOSESF = (217, 21, 17)
NORMSF = (34, 59, 199)
FEEDCOLOR = (190, 141, 217)

# Fonts
ENEMY_FONT = pygame.font.SysFont("Impact", 60)
PLAYER_FONT = pygame.font.SysFont("Zapfino", 36)
PLAYER_FONT2 = pygame.font.SysFont("Comic Sans", 20)
SCORE_FONT = pygame.font.SysFont("Verdana", 20)
OBJECTIVE_FONT = pygame.font.SysFont("Marker Felt", 15)
FEEDBACK_FONT = pygame.font.SysFont("Copperplate", 30)
FEEDMESSAGE_FONT = pygame.font.SysFont("Arial", 16)
FEEDINSTR_FONT = pygame.font.SysFont("Consolas", 16)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Game Title
pygame.display.set_caption("Space Invaders")

# Create classes
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(f"img/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = bullet_speed
    def update(self):
        self.rect.y -= self.speed
        if self.rect.top < -32:
            self.kill()

class Enemy_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"img/bullet.png")

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = 5
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(f"img/ufo-2.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = enemy_speed
    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left >= SCREEN_WIDTH:
            self.rect.right = 0
            self.rect.bottom += 10

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
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
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y): 
        super().__init__()
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

def feedback(feedbutton):
    pygame.draw.rect(screen, FEEDCOLOR, feedbutton)
    text3 = FEEDBACK_FONT.render('Leave us feedback!', True, WHITE)
    screen.blit(text3, (55, 55))
    

def feedbacksend(sender_email, sender_password, receiver_email, subject,
                 message):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(str(message), 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("An error occurred while sending the email. Error code " + str(e))

# Vars

spaceshipX = 400
spaceshipY = 500
enemy_num = 50
enemy_speed = 2
bullet_speed = 5
message = ""

# Game Loop
def main():
    global enemy_speed, bullet_speed,feedbutton, message
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
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
        enemy.speed = enemy_speed
        all_enemies.add(enemy)
        all_sprites.add(enemy)
    all_sprites.add(spaceship)

    running = True
    time_elapsed = 0

    enemy_state = "alive"
    player_state = "alive"
    tech_round = False
    feedback_mode = False
    score = 0
    bullet_sound = pygame.mixer.Sound(f"snd/SI #1.mp3")
    pygame.mixer.music.load(f"snd/Music.mp3")
    pygame.mixer.music.play(-1)
    text = SCORE_FONT.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (625, 20))
    objtext = OBJECTIVE_FONT.render("Achieve a score of 1000 to get a Tech Round!", True, WHITE)
    feedbutton = pygame.Rect(50, 50, 300, 50)
    
    while running:

        dt = clock.tick(fps)
        time_elapsed += dt
        keys = pygame.key.get_pressed()   
        if player_state == 'dead':
            screen.fill(YOULOSESF)
            text = ENEMY_FONT.render('Enemy Wins', True, BLACK)
            text2 = ENEMY_FONT.render('Press esc to exit', True, BLACK)
            screen.blit(text, (300, 300))
            screen.blit(text2, (330, 375))
            feedback(feedbutton)
        elif enemy_state == "alive":
            screen.fill(NORMSF)
        elif enemy_state == "dead":
            screen.fill(YOUWINSF)
            text = PLAYER_FONT.render('You Win!', True, YOUWINTC)
            text2 = PLAYER_FONT2.render('Press esc to exit', True, YOUWINTC)
            screen.blit(text, (300, 300))
            screen.blit(text2, (330, 375)) 
            feedback(feedbutton)
        screen.blit(objtext, (300, 25))
        if score >= 1000 and tech_round == False:
            tech_round = True
            objtext = OBJECTIVE_FONT.render("TECH ROUND", True, WHITE)
            screen.blit(objtext, (300, 25))
            enemy_speed += 5
            bullet_speed += 10
            for enemy in all_enemies:
                enemy.speed = enemy_speed
        text = SCORE_FONT.render("Score: " + str(score), True, WHITE)
        screen.blit(text, (625, 20))

        all_sprites.update()
        all_sprites.draw(screen)
        
        explosion_group.draw(screen)
        explosion_group.update()

        if time_elapsed >= 1000 and len(all_enemies) > 0:
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
                        bullet_sound.play()
                        bullet = Bullet(spaceship.rect.centerx, spaceship.rect.top)
                        all_sprites.add(bullet)
                        bullets.add(bullet)
            if event.type == pygame.MOUSEBUTTONDOWN and feedbutton.collidepoint(event.pos) and feedback_mode == False:
                feedback_mode = True
                
        if feedback_mode:
            pygame.mixer.music.fadeout(2000)
            while feedback_mode:
                for evt in pygame.event.get():
                    if evt.type == pygame.KEYDOWN:
                        if evt.key == pygame.K_BACKSPACE:
                            message = message[:-1]
                        elif evt.key == pygame.K_RETURN:
                            feedbacksend("goguesspython@gmail.com", "fsyp gmmp rarf xjwm", "goguesspython@gmail.com", "Space Invaders Feedback", message)
                            message = ""  # Clear message after sending
                            feedback_mode = False  # Exit feedback mode
                        else:
                            message += evt.unicode
                    elif evt.type == pygame.QUIT:
                        feedback_mode = False

                screen.fill(BLACK)

                # Render the instruction text
                instruction_text = "Enter your feedback. Press Enter to submit"
                instruction_block = FEEDINSTR_FONT.render(instruction_text, True, WHITE)
                instruction_rect = instruction_block.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 30))
                screen.blit(instruction_block, instruction_rect)

                # Render the input text
                block = FEEDMESSAGE_FONT.render(message, True, WHITE)
                rect = block.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                screen.blit(block, rect)
                pygame.display.flip()

        if player_state == "dead" or enemy_state == "dead":
            if keys[pygame.K_ESCAPE]:
                pygame.quit()

        s_e_collision = pygame.sprite.spritecollide(spaceship, all_enemies, False)
        
        for enemy in s_e_collision:
            explosion = Explosion(spaceship.rect.centerx, spaceship.rect.centery)
            if spaceship in all_sprites:

                explosion_group.add(explosion)
            spaceship.kill()
            all_sprites.remove(spaceship)
            player_state = "dead"
            
        b_e_collision = pygame.sprite.groupcollide(bullets, all_enemies, True, True)
        
        for enemy in b_e_collision:
            explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
            explosion_group.add(explosion)
            score += 100
        if len(all_enemies) == 0:
            enemy_state = "dead"

        eb_s_collision = pygame.sprite.spritecollide(spaceship, enemy_bullets, True)

        for enemybullet in eb_s_collision:
            explosion = Explosion(spaceship.rect.centerx, spaceship.rect.centery)
            if spaceship in all_sprites:
                explosion_group.add(explosion)
            spaceship.kill()
            all_sprites.remove(spaceship)
            player_state = "dead"
        pygame.display.flip()

if __name__ == "__main__":
    main()