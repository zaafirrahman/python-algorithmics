import pygame
import random

pygame.init()

# window
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clean The Earth 🌍")

clock = pygame.time.Clock()

# player
player = pygame.Rect(300, 200, 40, 40)
player_speed = 5

# trash
trash = pygame.Rect(random.randint(0, WIDTH-30), random.randint(0, HEIGHT-30), 30, 30)

# score & time
score = 0
font = pygame.font.SysFont(None, 36)
start_time = pygame.time.get_ticks()
game_duration = 30000  # 30 detik

running = True

while running:
    screen.fill((240, 240, 240))

    # cek exit
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

    # collision
    if player.colliderect(trash):
        score += 1
        trash.x = random.randint(0, WIDTH-30)
        trash.y = random.randint(0, HEIGHT-30)

    # timer
    elapsed = pygame.time.get_ticks() - start_time
    remaining = max(0, (game_duration - elapsed) // 1000)

    if remaining <= 0:
        running = False

    # draw objects
    pygame.draw.rect(screen, (0, 100, 255), player)  # player biru
    pygame.draw.rect(screen, (0, 200, 0), trash)     # sampah hijau

    # text
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    time_text = font.render(f"Time: {remaining}", True, (0, 0, 0))

    screen.blit(score_text, (10, 10))
    screen.blit(time_text, (10, 40))

    pygame.display.update()
    clock.tick(60)

# game over screen
screen.fill((255, 255, 255))
text = font.render(f"Game Over! Score: {score}", True, (0, 0, 0))
screen.blit(text, (200, 180))
pygame.display.update()

pygame.time.wait(3000)
pygame.quit()