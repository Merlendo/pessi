# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import random

pygame.init()  # Init the pygame engine

# Set the FPS
FPS = 120
CLOCK = pygame.time.Clock()

# Screen informations
WIDTH = 500
HEIGHT = 500

# Define colors
WHITE = (255, 255, 255)

# Create font
SCORE_FONT = pygame.font.SysFont('Courier New', 40, bold=True)

# Display the screen
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pessi")
ICO_PESSI = pygame.image.load("pessi.ico").convert()
pygame.display.set_icon(ICO_PESSI)

# Create the field
FIELD = pygame.image.load("grass_50.jpg").convert()

# Create pessi player
PESSI_WIDTH = 75
PESSI_HEIGHT = 100
PESSI_VEL = 5
PESSI_IMG = pygame.image.load("pessi.png").convert_alpha()
PESSI = pygame.transform.scale(PESSI_IMG, (PESSI_WIDTH, PESSI_HEIGHT))
pessi_rect = PESSI.get_rect(midbottom=(WIDTH // 2, HEIGHT))

# Create a ball
BALL_SIZE = 60
BALL_GRAVITY = -8
BALL_IMG = pygame.image.load("ball.png").convert_alpha()
BALL = pygame.transform.scale(BALL_IMG, (BALL_SIZE, BALL_SIZE))
gravity = 0
ball_vel_x = 0
pos_ball_start = random.uniform(0+BALL_SIZE, WIDTH-BALL_SIZE)
ball_rect = BALL.get_rect(midtop=(pos_ball_start, 0))

# Set the score
score = 0


def manage_ball_mouvement(gravity, ball_vel_x, score):
    """Check for collision between the ball and the pessi"""

    # Check for ball collision with the pessi
    if ball_rect.colliderect(pessi_rect) and ball_rect.bottom <= pessi_rect.top + 50:
        gravity = BALL_GRAVITY
        collision_angle = (ball_rect.centerx -
                           pessi_rect.centerx) / (PESSI_WIDTH / 2)
        ball_vel_x = ball_vel_x + collision_angle + random.uniform(-0.5, 0.5)
        score += 1

    # Check for ball collision with the border of the screen
    if ball_rect.left < 0 or ball_rect.right > WIDTH:
        ball_vel_x = -ball_vel_x

    # Check for ball colision whith the top of the screen
    if ball_rect.top < 0:
        gravity = -gravity
    gravity += 0.1
    ball_rect.y += gravity
    ball_rect.x += ball_vel_x
    return gravity, ball_vel_x, score


def reset_game(gravity, ball_vel_x, score):
    """Reset the pos of the pessi, ball and reset the score"""
    score = 0
    gravity = 0
    ball_vel_x = 0
    new_pos_ball_start = random.uniform(0+BALL_SIZE, WIDTH-BALL_SIZE)
    ball_rect.x = new_pos_ball_start
    ball_rect.y = 0
    pessi_rect.centerx = WIDTH//2
    return gravity, ball_vel_x, score


# Main game
run = True
game_active = True

while run:
    # Exit if the window is closed
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
    keys = pygame.key.get_pressed()

    # When the game is active
    if game_active:

        # Check if the pessi moves
        if keys[K_LEFT] and pessi_rect.left > 0:
            pessi_rect.x -= PESSI_VEL
        if keys[K_RIGHT] and pessi_rect.right < WIDTH:
            pessi_rect.x += PESSI_VEL

        # Manage the ball collision
        gravity, ball_vel_x, score = manage_ball_mouvement(
            gravity, ball_vel_x, score)

        # Get the score
        score_text = SCORE_FONT.render("Score: " + str(score), 1, WHITE)

        # Update screen
        SCREEN.blit(FIELD, (0, 0))
        SCREEN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 0))
        SCREEN.blit(PESSI, pessi_rect)
        SCREEN.blit(BALL, ball_rect)
        pygame.display.update()

        # Check if the ball fall
        if ball_rect.bottom > HEIGHT:
            game_active = False

    # When the game is game over
    else:
        # Print the game over screen
        SCREEN.blit(FIELD, (0, 0))
        SCREEN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 0))
        SCREEN.blit(PESSI, pessi_rect)
        SCREEN.blit(BALL, ball_rect)
        score_text_end = SCORE_FONT.render("Game Over", 1, WHITE)
        SCREEN.blit(score_text_end, (WIDTH//2 - score_text_end.get_width() //
                    2, HEIGHT//2 - score_text_end.get_height()//2))
        pygame.display.update()

        # Restart a game if the player press Enter
        if keys[K_RETURN]:
            gravity, ball_vel_x, score = reset_game(
                gravity, ball_vel_x, score)
            game_active = True

    # Limit the FPS
    CLOCK.tick(FPS)

pygame.quit()
