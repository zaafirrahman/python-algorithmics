import pygame
import random
import math
import os

# Init
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Shooter")
clock = pygame.time.Clock()

# Asset Path
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")

# Load Assets
player_img = pygame.image.load(os.path.join(ASSET_DIR, "player.png"))
player_img = pygame.transform.scale(player_img, (40, 40))

zombie_images = []
for i in range(1, 4):
    img = pygame.image.load(os.path.join(ASSET_DIR, f"zombie{i}.png"))
    img = pygame.transform.scale(img, (40, 40))
    zombie_images.append(img)

# Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

# Player
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 5
health = 100
score = 0

# Bullets
bullets = []
bullet_speed = 10

# Zombies
zombies = []
zombie_speed = 1.5
spawn_timer = 0

font = pygame.font.SysFont(None, 30)


def spawn_zombie():
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        pos = [random.randint(0, WIDTH), 0]
    elif side == "bottom":
        pos = [random.randint(0, WIDTH), HEIGHT]
    elif side == "left":
        pos = [0, random.randint(0, HEIGHT)]
    else:
        pos = [WIDTH, random.randint(0, HEIGHT)]

    img = random.choice(zombie_images)
    return {"pos": pos, "img": img}


running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            dx = mx - player_pos[0]
            dy = my - player_pos[1]
            dist = math.hypot(dx, dy)
            if dist != 0:
                dx, dy = dx / dist, dy / dist
                bullets.append([player_pos[0], player_pos[1], dx, dy])

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos[1] -= player_speed
    if keys[pygame.K_s]:
        player_pos[1] += player_speed
    if keys[pygame.K_a]:
        player_pos[0] -= player_speed
    if keys[pygame.K_d]:
        player_pos[0] += player_speed

    # Spawn zombies
    spawn_timer += 1
    if spawn_timer > 60:
        zombies.append(spawn_zombie())
        spawn_timer = 0

    # Update zombies
    for z in zombies[:]:
        pos = z["pos"]
        dx = player_pos[0] - pos[0]
        dy = player_pos[1] - pos[1]
        dist = math.hypot(dx, dy)
        if dist != 0:
            pos[0] += zombie_speed * dx / dist
            pos[1] += zombie_speed * dy / dist

        # Collision with player
        if dist < 30:
            health -= 1
            zombies.remove(z)

    # Update bullets
    for b in bullets[:]:
        b[0] += b[2] * bullet_speed
        b[1] += b[3] * bullet_speed

        if b[0] < 0 or b[0] > WIDTH or b[1] < 0 or b[1] > HEIGHT:
            bullets.remove(b)
            continue

        for z in zombies[:]:
            pos = z["pos"]
            if math.hypot(b[0] - pos[0], b[1] - pos[1]) < 20:
                zombies.remove(z)
                bullets.remove(b)
                score += 1
                break

    # Draw player
    screen.blit(player_img, (player_pos[0] - 20, player_pos[1] - 20))

    # Draw bullets
    for b in bullets:
        pygame.draw.circle(screen, WHITE, (int(b[0]), int(b[1])), 4)

    # Draw zombies
    for z in zombies:
        pos = z["pos"]
        img = z["img"]
        screen.blit(img, (pos[0] - 20, pos[1] - 20))

    # UI
    health_text = font.render(f"Health: {health}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(health_text, (10, 10))
    screen.blit(score_text, (10, 40))

    if health <= 0:
        game_over = font.render("GAME OVER", True, RED)
        screen.blit(game_over, (WIDTH // 2 - 60, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False

    pygame.display.flip()

pygame.quit()