#   Space Invaders Clone by Obadah Ghizawi, 2022
#   Don't reuse code without consent

import pygame as pg
import random
import math
from pygame import mixer

#   pygame initialization
pg.init()

#   Creating window
screen = pg.display.set_mode((1000, 667))

#   Background
background = pg.image.load('space.jpg')

#   Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)

#   Title and Icon
pg.display.set_caption("Space Invaders")
icon = pg.image.load('ufo.png')
pg.display.set_icon(icon)

#   Player
playerImg = pg.image.load('player.png')
playerX = 470
playerY = 500
playerX_change = 0

#   Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pg.image.load('alien.png'))
    enemyX.append(random.randint(0, 935))
    enemyY.append(random.randint(100, 200))
    enemyX_change.append(0.15)
    enemyY_change.append(40)

#   Bullet
bulletImg = pg.image.load('bullet.png')
bulletX = 0
bulletY = 500
bulletX_change = 0
bulletY_change = 0.6
bullet_state = "Ready"

#   Score

score_value = 0
font = pg.font.Font('freesansbold.ttf', 25)
textX = 10
textY = 10

#   Game Over Text
over_font = pg.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = over_font.render("Game Over! Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, index):
    screen.blit(enemyImg[index], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(ex, ey, bx, by):
    distance = math.sqrt((math.pow((ex - bx), 2)) + (math.pow((ey - by), 2)))
    if distance < 27:
        return True
    else:
        return False


#   Game loop
running = True
while running:
    #   RGB fill
    screen.fill((0, 0, 0))
    #   Background image
    screen.blit(background, (0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        #   if key is pressed, check whether it's left or right
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                playerX_change = -0.3
            if event.key == pg.K_RIGHT:
                playerX_change = 0.3
            if event.key == pg.K_SPACE:
                if bullet_state == "Ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                playerX_change = 0
    #   Boundary checks for spaceship & enemy
    #   Player Movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 936:
        playerX = 936

    #   Enemy Movement
    for i in range(num_of_enemies):
        #   Game Over
        if enemyY[i] > 460:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 936:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
            #   Collision Check
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = "Ready"
            score_value += 1
            enemyX[i] = random.randint(0, 935)
            enemyY[i] = random.randint(100, 200)

        enemy(enemyX[i], enemyY[i], i)

    #   Bullet Movement
    if bulletY <= 0:
        bulletY = 500
        bullet_state = "Ready"

    if bullet_state == "Fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pg.display.update()
