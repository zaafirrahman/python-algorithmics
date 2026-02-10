import pygame
import random
import sys

# Inisialisasi pygame
pygame.init()

# Ukuran layar
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Survival Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Warna
BLUE = (0, 120, 255)
RED = (200, 0, 0)
WHITE = (255, 255, 255)

# Player
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - 70
player_speed = 6
player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

# Musuh
enemy_size = 40
enemy_x = random.randint(0, WIDTH - enemy_size)
enemy_y = -enemy_size
enemy_speed = 5
enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)

# Score
score = 0
score_timer = pygame.USEREVENT
pygame.time.set_timer(score_timer, 1000)  # tiap 1 detik

# Game loop
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == score_timer:
            score += 1

    # Input player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += player_speed

    # Gerak musuh
    enemy_rect.y += enemy_speed
    if enemy_rect.top > HEIGHT:
        enemy_rect.y = -enemy_size
        enemy_rect.x = random.randint(0, WIDTH - enemy_size)

    # Collision
    if player_rect.colliderect(enemy_rect):
        running = False

    # Gambar objek
    pygame.draw.rect(screen, BLUE, player_rect)
    pygame.draw.rect(screen, RED, enemy_rect)

    # Tampilkan score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.update()

# Game over screen
screen.fill(WHITE)
game_over_text = font.render("Game Over", True, (0, 0, 0))
final_score_text = font.render(f"Final Score: {score}", True, (0, 0, 0))
screen.blit(game_over_text, (WIDTH//2 - 80, HEIGHT//2 - 40))
screen.blit(final_score_text, (WIDTH//2 - 100, HEIGHT//2))
pygame.display.update()

pygame.time.delay(3000)
pygame.quit()
