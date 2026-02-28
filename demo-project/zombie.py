import pygame
import random
import math
import os

pygame.init()

# =========================
# AUTO RELATIVE PATH
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "assets")

def load_image(name, size=None):
    """Load image dengan relative path + auto scale"""
    path = os.path.join(ASSETS, name)
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except:
        print(f"Gagal load {name}")
        return None

# =========================
# SETUP
# =========================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Shooter")

clock = pygame.time.Clock()

WHITE = (255,255,255)
RED = (200,0,0)
GREEN = (0,200,0)
BLACK = (0,0,0)

font = pygame.font.SysFont(None, 36)

# =========================
# LOAD IMAGES
# =========================
background_img = load_image("landscape.png", (WIDTH, HEIGHT))
player_img = load_image("player.png", (40, 40))

zombie_images = [
    load_image("zombie1.png", (40, 40)),
    load_image("zombie2.png", (40, 40)),
    load_image("zombie3.png", (40, 40))
]

# =========================
# PLAYER
# =========================
player_size = 40
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 5
player_hp = 100

# =========================
# BULLETS
# =========================
bullets = []
bullet_speed = 10
bullet_radius = 5

# =========================
# ZOMBIES
# =========================
zombies = []
zombie_speed = 1.5
spawn_timer = 0

score = 0
game_over = False

# =========================
# FUNCTIONS
# =========================
def spawn_zombie():
    side = random.choice(["top","bottom","left","right"])

    if side == "top":
        x = random.randint(0, WIDTH)
        y = -50
    elif side == "bottom":
        x = random.randint(0, WIDTH)
        y = HEIGHT + 50
    elif side == "left":
        x = -50
        y = random.randint(0, HEIGHT)
    else:
        x = WIDTH + 50
        y = random.randint(0, HEIGHT)

    img = random.choice(zombie_images)
    zombies.append([x, y, img])

def draw_text(text, x, y):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x,y))

# =========================
# GAME LOOP
# =========================
running = True

while running:

    clock.tick(60)

    # DRAW BACKGROUND
    if background_img:
        screen.blit(background_img, (0,0))
    else:
        screen.fill(BLACK)

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mx, my = pygame.mouse.get_pos()

            dx = mx - player_x
            dy = my - player_y
            dist = math.hypot(dx, dy)

            if dist != 0:
                dx, dy = dx/dist, dy/dist
                bullets.append([player_x, player_y, dx, dy])

    keys = pygame.key.get_pressed()

    if not game_over:
        # PLAYER MOVE
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player_y += player_speed

        player_x = max(0, min(WIDTH, player_x))
        player_y = max(0, min(HEIGHT, player_y))

        # SPAWN ZOMBIE
        spawn_timer += 1
        if spawn_timer > 60:
            spawn_zombie()
            spawn_timer = 0

        # UPDATE BULLETS
        for bullet in bullets[:]:
            bullet[0] += bullet[2] * bullet_speed
            bullet[1] += bullet[3] * bullet_speed

            if bullet[0] < 0 or bullet[0] > WIDTH or bullet[1] < 0 or bullet[1] > HEIGHT:
                bullets.remove(bullet)

        # UPDATE ZOMBIES
        for zombie in zombies[:]:
            zx, zy, img = zombie

            dx = player_x - zx
            dy = player_y - zy
            dist = math.hypot(dx, dy)

            if dist != 0:
                zx += dx/dist * zombie_speed
                zy += dy/dist * zombie_speed

            zombie[0], zombie[1] = zx, zy

            if dist < 30:
                player_hp -= 1

        # COLLISION
        for zombie in zombies[:]:
            zx, zy, _ = zombie
            for bullet in bullets[:]:
                if math.hypot(zx-bullet[0], zy-bullet[1]) < 25:
                    zombies.remove(zombie)
                    bullets.remove(bullet)
                    score += 1
                    break

        if player_hp <= 0:
            game_over = True

    # =========================
    # DRAW OBJECTS
    # =========================

    # PLAYER
    if player_img:
        screen.blit(player_img, (player_x-20, player_y-20))
    else:
        pygame.draw.circle(screen, GREEN, (int(player_x), int(player_y)), 20)

    # BULLETS
    for bullet in bullets:
        pygame.draw.circle(screen, WHITE, (int(bullet[0]), int(bullet[1])), bullet_radius)

    # ZOMBIES
    for zx, zy, img in zombies:
        if img:
            screen.blit(img, (zx, zy))
        else:
            pygame.draw.rect(screen, RED, (zx, zy, 30, 30))

    # UI
    draw_text(f"HP: {player_hp}", 10, 10)
    draw_text(f"Score: {score}", 10, 40)

    if game_over:
        draw_text("GAME OVER", WIDTH//2 - 100, HEIGHT//2)

    pygame.display.flip()

pygame.quit()