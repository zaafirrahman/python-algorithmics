import pygame
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

pygame.init()

# ===== WINDOW =====
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clean The Earth 🌍")

clock = pygame.time.Clock()

# ===== LOAD IMAGES =====
bg_img = pygame.image.load(BASE_DIR / "landscape.png")
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

player_img = pygame.image.load(BASE_DIR / "player.png")
player_img = pygame.transform.scale(player_img, (60, 60))

# list semua sampah
trash_images = []
for i in range(1, 6):
    img = pygame.image.load(BASE_DIR / f"bin{i}.png")
    img = pygame.transform.scale(img, (40, 40))
    trash_images.append(img)

# ===== PLAYER =====
player = player_img.get_rect(center=(WIDTH//2, HEIGHT//2))
player_speed = 5

# ===== TRASH =====
def spawn_trash():
    img = random.choice(trash_images)
    rect = img.get_rect(
        center=(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50))
    )
    return img, rect

trash_img, trash_rect = spawn_trash()

# ===== SCORE & TIMER ====
score = 0
font = pygame.font.SysFont(None, 40)

start_time = pygame.time.get_ticks()
game_duration = 60000  # 60 second

running = True

# ===== GAME LOOP =====
while running:

    # background
    screen.blit(bg_img, (0, 0))

    # exit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
    if keys[pygame.K_UP]:
        player.y -= player_speed
    if keys[pygame.K_DOWN]:
        player.y += player_speed

    # batas layar
    player.clamp_ip(screen.get_rect())

    # collision
    if player.colliderect(trash_rect):
        score += 1
        trash_img, trash_rect = spawn_trash()

    # timer
    elapsed = pygame.time.get_ticks() - start_time
    remaining = max(0, (game_duration - elapsed) // 1000)

    if remaining <= 0:
        running = False

    # draw objects
    screen.blit(player_img, player)
    screen.blit(trash_img, trash_rect)

    # text
    score_text = font.render(f"Score: {score}", True, (0,0,0))
    time_text = font.render(f"Time: {remaining}", True, (0,0,0))

    screen.blit(score_text, (20, 20))
    screen.blit(time_text, (20, 60))

    pygame.display.update()
    clock.tick(60)

# ===== GAME OVER =====
screen.fill((255,255,255))
text = font.render(f"Game Over! Score: {score}", True, (0,0,0))
screen.blit(text, (WIDTH//2-150, HEIGHT//2))
pygame.display.update()

pygame.time.wait(3000)
pygame.quit()