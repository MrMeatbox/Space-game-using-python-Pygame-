import random

import pygame

# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.jpg")

# Title and logo
pygame.display.set_caption("CSE-346 Project")
icon = pygame.image.load("cuet.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("spaceship_hero.png")
playerX = 370
playerY = 480
playerX_change = 0

# Alien
enemyImg = pygame.image.load("alien2.png")
enemyX = random.randint(0, 736)
enemyY = random.randint(20, 150)
enemyX_change = 0.3
enemyY_change = 30

# Bullets
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
# bulletX_change = 0.3
bulletY_change = 2
bullet_state = "ready"


# we cannot see the bullet when ready
# we can see the bullet when fire


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y + 10))


# Game Loop
running = True
while running:

    # RGB - Red, Green, Blue
    screen.fill((255, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    # playerX -= .2
    # print(playerX)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # player boundary
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy boundary
    enemyX += enemyX_change

    if enemyX <= 0:
        enemyX_change = 0.1
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -0.1
        enemyY += enemyY_change

    # bullet movement
    if bulletY <= 0 :
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()
