import math

import pygame
import random

# Initialize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background.png')

# caption and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('controlJuego.png')
pygame.display.set_icon(icon)

# player
score = 0
playerImg = pygame.image.load('astronave.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemigo.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# bullet
bulletImg = pygame.image.load('bullet.png')  # no usa X
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"  # ready -> no visible     fire -> visible

#Font
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score1 = font.render('Score: ' + str(score), True, (255, 255, 255))
    screen.blit(score1, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER ", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state  # para poder accederlo desde la funcion
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # para que salga de "arriba" de la nave


def isCollision(enemyX, enemY, bulletX, bulletY):
    distance = math.sqrt(math.pow((bulletX - enemyX), 2) + (math.pow((bulletY - enemY), 2)))
    return distance < 36

def isCollisionSpaceship(enemyX, enemY, playerX, playerY):
    distance = math.sqrt(math.pow((playerX - enemyX), 2) + (math.pow((playerY - enemY), 2)))
    return distance < 36


# game loop
running = True
while running:  # agarra todos los eventos ingame uno por uno en el for y checkea si le dio a quit

    screen.fill((0, 124, 140))  # RGB
    screen.blit(background, (0, 0))  # background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed, check wether its rigth of left
        if event.type == pygame.KEYDOWN:  # pressing key up, down, left, right (movement)
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_UP:
                playerY_change = -5
            if event.key == pygame.K_DOWN:
                playerY_change = 5
            if event.key == pygame.K_SPACE:  # " pacaum pacaum pacaum " -la bala.  "tucun tucun tucun" -el corazon
                if bullet_state == "ready":
                    bulletX = playerX  # dispara desde la posicion actual de la bala
                    bulletY = playerY
                    fire_bullet(playerX, playerY)

        if event.type == pygame.KEYUP:  # releasing key
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0

    # cambios en movimiento de player
    playerX += playerX_change
    playerY += playerY_change

    # ------se "teletransporta" en los limites. En realidad solo resetea el lugar de la nave------
    if playerX <= -35:  # segun el tamano de la nave
        playerX = 800
    elif playerX >= 800:
        playerX = 0

    if playerY <= -35:
        playerY = 600
    elif playerY >= 600:
        playerY = 0

    playerX += playerX_change
    playerY += playerY_change
    # --------------------------------------------------------------

    # --------- cambios en movimiento de enemy ---------------------

    for i in range(num_of_enemies):

        #   GAME OVER!!!  porque llegaron a abajo o chocaron con la nave
        if enemyY[i] > 440 or isCollisionSpaceship(enemyX[i], enemyY[i], playerX, playerY):
            for j in range(num_of_enemies):
                enemyY[j] =  2000 # para que se vayan a abajo de la pantalla
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        # enemyY += enemyY_change

        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # if enemyY[i] <= -35:
        #     enemyY[i] = 600
        # elif enemyY[i] >= 600:
        #     enemyY[i] = 0

        # --collision detection para cada enemy--
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)  # respawnea la bala y el enemy
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score += 1
            print(score)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # --------------------------------------------------------------

    # -------movimiento de la bala-------------------

    if bulletY <= 0:  # se resetea cuando sale de la pantalla
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # ---------------------------------------------------------------



    # ---------------------------------------------------------------

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()







