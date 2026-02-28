import pygame
import random
import math

pygame.init()

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
# PLAYER
# =========================
player_size = 30
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
zombie_size = 30
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

    zombies.append([x,y])

def draw_text(text, x, y):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x,y))

# =========================
# GAME LOOP
# =========================
running = True

while running:

    clock.tick(60)
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

        # BATASI AREA
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
            dx = player_x - zombie[0]
            dy = player_y - zombie[1]
            dist = math.hypot(dx, dy)

            if dist != 0:
                zombie[0] += dx/dist * zombie_speed
                zombie[1] += dy/dist * zombie_speed

            # tabrak player
            if dist < 25:
                player_hp -= 1

        # COLLISION BULLET vs ZOMBIE
        for zombie in zombies[:]:
            for bullet in bullets[:]:
                if math.hypot(zombie[0]-bullet[0], zombie[1]-bullet[1]) < 20:
                    zombies.remove(zombie)
                    bullets.remove(bullet)
                    score += 1
                    break

        # GAME OVER
        if player_hp <= 0:
            game_over = True

    # =========================
    # DRAW OBJECTS
    # =========================

    # player
    pygame.draw.circle(screen, GREEN, (int(player_x), int(player_y)), player_size//2)

    # bullets
    for bullet in bullets:
        pygame.draw.circle(screen, WHITE, (int(bullet[0]), int(bullet[1])), bullet_radius)

    # zombies
    for zombie in zombies:
        pygame.draw.rect(screen, RED, (zombie[0], zombie[1], zombie_size, zombie_size))

    # UI
    draw_text(f"HP: {player_hp}", 10, 10)
    draw_text(f"Score: {score}", 10, 40)

    if game_over:
        draw_text("GAME OVER", WIDTH//2 - 100, HEIGHT//2)

    pygame.display.flip()

pygame.quit()