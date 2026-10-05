# Full 2D Endless Runner Prototype (1–7 Complete)
# Python + Pygame | No Game Engine
# pip install pygame

import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 960, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Adventure Runner")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# ------------------ COLORS ------------------
WHITE = (240, 240, 240)
BLACK = (20, 20, 20)
RED = (200, 60, 60)
BLUE = (70, 140, 230)
GRAY = (80, 80, 80)

# ------------------ PLAYER SPRITE (SINGLE FRAME) ------------------
# Using ONE running frame only (no constant movement)
SPRITE_SHEET_PATH = "runner_sprites.png"
sprite_sheet = pygame.image.load(SPRITE_SHEET_PATH).convert_alpha()

FRAME_WIDTH = 256
FRAME_HEIGHT = 256

# Pick ONE clean running frame (row 0, column 2)
player_image = sprite_sheet.subsurface(
    2 * FRAME_WIDTH,
    0 * FRAME_HEIGHT,
    FRAME_WIDTH,
    FRAME_HEIGHT
)
player_image = pygame.transform.scale(player_image, (48, 72))

# ------------------ SOUNDS (HOOKS) ------------------
jump_sound = None
hit_sound = None
boss_sound = None

# ------------------ PLAYER ------------------
player = pygame.Rect(100, HEIGHT - 110, 48, 72)
# Timed jump variables (no continuous gravity)
is_jumping = False
jump_timer = 0
JUMP_UP_FRAMES = 12
JUMP_UP_SPEED = 20
JUMP_HANG_FRAMES = 8
JUMP_DOWN_SPEED = 18
on_ground = True
ducking = False
anim = 0
health = 3

# ------------------ BACKGROUND (LOOPING IMAGE) ------------------
BG_IMAGE_PATH = "background.png"  # rename the city image to this
bg_image = pygame.image.load(BG_IMAGE_PATH).convert()
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

bg_x1 = 0
bg_x2 = WIDTH
bg_speed = 2

# ------------------ WORLD ------------------
obstacles = []
speed = 6
distance = 0
level = 1
ob_timer = 0

# ------------------ FUNCTIONS ------------------
def draw_text(t, x, y, c=WHITE):
    # Draw a small shadow for better contrast on any background
    shadow = font.render(t, True, BLACK)
    screen.blit(shadow, (x + 1, y + 1))
    screen.blit(font.render(t, True, c), (x, y))


def reset_game():
    global obstacles, speed, distance, level, health
    obstacles.clear()
    speed = 6
    distance = 0
    level = 1
    health = 3
    player.bottom = HEIGHT - 40

# ------------------ GAME LOOP ------------------
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Jump (start timed jump)
    if keys[pygame.K_SPACE] and on_ground:
        is_jumping = True
        jump_timer = 0
        on_ground = False

    # Duck
    if keys[pygame.K_DOWN] and on_ground:
        ducking = True
        player.height = 42
        player.bottom = HEIGHT - 40
    else:
        ducking = False
        player.height = 72
        player.bottom = HEIGHT - 40

    # Jump physics (timed jump with hang time)
    if is_jumping:
        if jump_timer < JUMP_UP_FRAMES:
            player.y -= JUMP_UP_SPEED
        elif jump_timer < JUMP_UP_FRAMES + JUMP_HANG_FRAMES:
            # Hang time at the top: no vertical movement
            pass
        else:
            player.y += JUMP_DOWN_SPEED
        jump_timer += 1
    else:
        # If somehow in air without jump, bring player down at fixed speed
        if player.bottom < HEIGHT - 40:
            player.y += JUMP_DOWN_SPEED

    if player.bottom >= HEIGHT - 40:
        player.bottom = HEIGHT - 40
        is_jumping = False
        jump_timer = 0
        on_ground = True

    # Spawn obstacles
    ob_timer += 1
    if ob_timer > max(45, 90 - level * 8):
        ob_timer = 0
        if random.choice([True, False]):
            obstacles.append(pygame.Rect(WIDTH, HEIGHT - 80, 36, 40))
        else:
            obstacles.append(pygame.Rect(WIDTH, HEIGHT - 150, 36, 36))

    # (No enemies or boss in this simplified endless runner)

    # Move entities
    for o in obstacles: o.x -= speed

    obstacles = [o for o in obstacles if o.x > -60]

    # Collisions
    for ent in obstacles:
        if player.colliderect(ent):
            health -= 1
            ent.x = -100

    if health <= 0:
        reset_game()

    # Progression
    distance += 1
    if distance % 900 == 0:
        level += 1
        speed += 1

    # Draw scrolling background
    bg_x1 -= bg_speed
    bg_x2 -= bg_speed
    if bg_x1 <= -WIDTH:
        bg_x1 = WIDTH
    if bg_x2 <= -WIDTH:
        bg_x2 = WIDTH

    screen.blit(bg_image, (bg_x1, 0))
    screen.blit(bg_image, (bg_x2, 0))


    # Draw player
    screen.blit(player_image, player)
    for o in obstacles: pygame.draw.rect(screen, RED, o)

    pygame.draw.rect(screen, BLACK, (0, HEIGHT - 40, WIDTH, 40))

    draw_text(f"Distance: {distance}", 20, 20)
    draw_text(f"Level: {level}", 20, 45)
    draw_text(f"Health: {health}", 20, 70)
    draw_text("SPACE=Jump  DOWN=Duck", 20, 95)

    pygame.display.update()
