import pygame
import random
import math
from pygame import mixer   # to add music

# initialize pygame
pygame.init()

# screen
SCREEN_WIDTH = 996
SCREEN_HEIGHT = 558

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# background
backImg = pygame.image.load('back.png')

# background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# icon and caption
pygame.display.set_caption("Space invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('spaceship.png')
playerX = 400
playerY = 490
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 5

base_enemy_speed = 1
enemy_speed_increment = 0.3

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 932))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(base_enemy_speed)
    enemyY_change.append(100)

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 490
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# score
score_val = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_val), True, (255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (320, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))  # blit- to draw

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# game loop
run = True
while run:

    screen.fill((0, 0, 0))
    screen.blit(backImg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = +2
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("bullet.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX > 932:
        playerX = 932

    # enemy movement
    for i in range(no_of_enemies):

        # game over
        if enemyY[i] > 450:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = base_enemy_speed + score_val * enemy_speed_increment
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 932:
            enemyX_change[i] = -(base_enemy_speed + score_val * enemy_speed_increment)
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 490
            bullet_state = "ready"
            score_val += 1
            enemyX[i] = random.randint(0, 932)
            enemyY[i] = random.randint(0, 150)
            enemyX_change[i] = base_enemy_speed + score_val * enemy_speed_increment if enemyX_change[i] > 0 else -(base_enemy_speed + score_val * enemy_speed_increment)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 490
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
