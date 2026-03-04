import pygame
import random
import math

# Init
pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Shooter")

clock = pygame.time.Clock()

# Colors
WHITE = (255,255,255)
RED = (200,0,0)
GREEN = (0,200,0)
BLACK = (0,0,0)

# Player
player_pos = [WIDTH//2, HEIGHT//2]
player_speed = 5
player_radius = 20

# Bullets
bullets = []
bullet_speed = 10
bullet_radius = 5

# Zombies
zombies = []
zombie_speed = 2
zombie_radius = 20
spawn_timer = 0

# Score
score = 0
font = pygame.font.SysFont(None, 36)

running = True
game_over = False

while running:
    clock.tick(60)
    screen.fill((30,30,30))

    if not game_over:

        # Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                angle = math.atan2(my - player_pos[1], mx - player_pos[0])
                bullets.append([
                    player_pos[0],
                    player_pos[1],
                    math.cos(angle) * bullet_speed,
                    math.sin(angle) * bullet_speed
                ])

        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player_pos[1] -= player_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player_pos[1] += player_speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player_pos[0] -= player_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player_pos[0] += player_speed

        # Spawn Zombie
        spawn_timer += 1
        if spawn_timer > 60:
            spawn_timer = 0
            side = random.choice(["top","bottom","left","right"])
            if side == "top":
                zombies.append([random.randint(0,WIDTH), 0])
            elif side == "bottom":
                zombies.append([random.randint(0,WIDTH), HEIGHT])
            elif side == "left":
                zombies.append([0, random.randint(0,HEIGHT)])
            else:
                zombies.append([WIDTH, random.randint(0,HEIGHT)])

        # Update Bullets
        for bullet in bullets[:]:
            bullet[0] += bullet[2]
            bullet[1] += bullet[3]

            if bullet[0] < 0 or bullet[0] > WIDTH or bullet[1] < 0 or bullet[1] > HEIGHT:
                bullets.remove(bullet)

        # Update Zombies
        for zombie in zombies[:]:
            angle = math.atan2(player_pos[1] - zombie[1], player_pos[0] - zombie[0])
            zombie[0] += math.cos(angle) * zombie_speed
            zombie[1] += math.sin(angle) * zombie_speed

            # Check collision with player
            dist = math.hypot(player_pos[0] - zombie[0], player_pos[1] - zombie[1])
            if dist < player_radius + zombie_radius:
                game_over = True

            # Check collision with bullet
            for bullet in bullets[:]:
                dist = math.hypot(bullet[0] - zombie[0], bullet[1] - zombie[1])
                if dist < bullet_radius + zombie_radius:
                    if zombie in zombies:
                        zombies.remove(zombie)
                    if bullet in bullets:
                        bullets.remove(bullet)
                    score += 1
                    break

        # Draw Player
        pygame.draw.circle(screen, GREEN, (int(player_pos[0]), int(player_pos[1])), player_radius)

        # Draw Bullets
        for bullet in bullets:
            pygame.draw.circle(screen, WHITE, (int(bullet[0]), int(bullet[1])), bullet_radius)

        # Draw Zombies
        for zombie in zombies:
            pygame.draw.circle(screen, RED, (int(zombie[0]), int(zombie[1])), zombie_radius)

        # Draw Score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10,10))

    else:
        over_text = font.render("GAME OVER - Press R to Restart", True, RED)
        screen.blit(over_text, (WIDTH//2 - 180, HEIGHT//2))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            player_pos = [WIDTH//2, HEIGHT//2]
            bullets.clear()
            zombies.clear()
            score = 0
            game_over = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.display.flip()

pygame.quit()