import random
import math
import pygame
from pygame import mixer


# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# explosion

blast = pygame.image.load("explode.png")

# Background
background = pygame.image.load("background1800x600.jpg")

# Backgrounf game
mixer.music.load("bg-1.mp3")
mixer.music.play(-1)

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
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 12

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("alien2.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(20, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(30)

# Bullets
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
# bulletX_change = 0.3
bulletY_change = 4
bullet_state = "ready"


#score

score_value = 0
font = pygame.font.Font('Game Space Academy.otf', 40)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('Game Space Academy.otf', 64)

# Pause
pause_font = pygame.font.Font("Game Space Academy.otf", 75)
press_pause = pygame.font.Font("Game Space Academy.otf", 30)
def pause():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        pause = pause_font.render("Paused!", True, (0, 0, 255))
        message1 = font.render("Press C to continue", True, (255, 255, 0))
        message2 = font.render("Press Q to Quit", True, (255, 255, 0))
        screen.blit(pause, (300, 160))
        screen.blit(message1, (270, 260))
        screen.blit(message2, (290, 300))

        pygame.display.update()



def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 0, 0))
    screen.blit(score, (x, y))


#Shoe message
def show_message():
    press = press_pause.render("Press P to pause", True, (255, 255, 255))
    screen.blit(press, (630, 10))
def high_score(x, y):
    score = font.render("High Score: " + str(highest_score), True, (255, 0, 0))
    screen.blit(score, (x, y))

# we cannot see the bullet when ready
# we can see the bullet when fire

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    player_score = font.render("Your Score: "+str(score_value), True, (255, 255, 0))
    h_score = font.render("Higest score: "+str(highest_score), True, (255, 0, 0))
    screen.blit(over_text, (270, 250))
    screen.blit(player_score, (300, 350))
    screen.blit(h_score, (300, 380))

def player(x, y):
    screen.blit(playerImg, (x, y))

#show High score
def for_high_score():
    with open("high Score.txt", "r") as f:
        return f.read()


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y + 10))

def blastFire(x, y):
    screen.blit(blast, (x, y))

try:
    highest_score = int(for_high_score())
except:
    highest_score = 0

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

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
                    bullet_sound = mixer.Sound("blaster.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire(bulletX, bulletY)
            if event.key == pygame.K_p:
                pause()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # player boundary
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement

    for i in range(num_of_enemies):

        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000

            game_over_text()
            break
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            # 0.3
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            blastFire(enemyX[i], enemyY[i])
            explode = mixer.Sound("explode.mp3")
            explode.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(20, 150)
            print(score_value)

        enemy(enemyX[i], enemyY[i], i)


    # check high score
    if(highest_score < score_value):
        highest_score = score_value
    with open("high Score.txt","w") as f:
        f.write(str(highest_score))
    # bullet movement
    if bulletY <= 0 :
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire(bulletX, bulletY)
        bulletY -= bulletY_change



    player(playerX, playerY)
    show_score(textX, textY)
    high_score(10, 50)
    show_message()
    pygame.display.update()
