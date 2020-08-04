import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# creates a screen
screen = pygame.display.set_mode((800, 600))

# Background
backgound = pygame.image.load('background.png')

#Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Caption And Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load('space-invaders.png')
PlayerX = 370
PlayerY = 480
PlayerX_change = 0

# Enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = int(input("How many enemies do you want"))
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
# Ready - "You can't see the bullet on the screen"
# Fire - "The bullet is currently moving"
Bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 12
bullet_state = "ready"

#Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

# Game Over Text

over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    score = font.render("Score  :  " + str(score_value),True, (255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = font.render('GAME OVER !!!!',True, (255,0,0))
    screen.blit(over_text, (200, 250))


# Drawing the player image
def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y,i):
    screen.blit(enemyimg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(Bulletimg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:

    # RGB - Red  Green  Blue
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(backgound, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed to check wether it is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PlayerX_change = -5

            if event.key == pygame.K_RIGHT:
                PlayerX_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    # Gets the X coordinate of the spaceship
                    bulletX = PlayerX

                fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                PlayerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 -0.1
    # 5 = 5 + 0.1

    # Checking for boundaries of spaceship so it doesn't go out of bounds
    PlayerX += PlayerX_change
    if PlayerX <= 0:
        PlayerX = 0

    elif PlayerX >= 740:
        PlayerX = 740

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 435:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(PlayerX, PlayerY)
    show_score(textX, textY)
    pygame.display.update()
