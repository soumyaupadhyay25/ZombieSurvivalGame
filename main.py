import pygame
import sys
import os
import math
import random
import time

# Initialize PyGame
pygame.init()
pygame.mixer.init()

# Screen Settings
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival Game")
clock = pygame.time.Clock()

# Load assets
ASSETS = os.path.join(os.path.dirname(__file__), "assets")
PLAYER_IMAGE = pygame.image.load(os.path.join(ASSETS, "player.png"))
PLAYER_IMAGE = pygame.transform.scale(PLAYER_IMAGE, (50, 50))

ZOMBIE_IMAGE = pygame.image.load(os.path.join(ASSETS, "zombie.png"))
ZOMBIE_IMAGE = pygame.transform.scale(ZOMBIE_IMAGE, (50, 50))

BULLET_IMAGE = pygame.image.load(os.path.join(ASSETS, "bullet.png"))
BULLET_IMAGE = pygame.transform.scale(BULLET_IMAGE, (15, 15))

# Sounds
shoot_sound = pygame.mixer.Sound("assets/sounds/shoot.mp3")
zombie_hit_sound = pygame.mixer.Sound("assets/sounds/zombie_hit.wav")
player_hit_sound = pygame.mixer.Sound("assets/sounds/player_hit.wav")
game_over_sound = pygame.mixer.Sound("assets/sounds/game_over.wav")

shoot_sound.set_volume(0.5)
zombie_hit_sound.set_volume(0.6)
player_hit_sound.set_volume(0.6)
game_over_sound.set_volume(0.7)

# Background music
pygame.mixer.music.load("assets/sounds/background.mp3")
pygame.mixer.music.play(-1)  # Loop forever
pygame.mixer.music.set_volume(0.4)

# Player Setup
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 5
bullet_speed = 10
zombie_speed = 1.2
bullets = []
zombies = []
score = 0
splatters = []
font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 60)

player_health = 100
game_over = False
zombie_spawn_timer = 0

# Spawn Zombie at random edge
def spawn_zombie():
    edge = random.choice(['top', 'bottom', 'left', 'right'])
    if edge == 'top':
        return [random.randint(0, WIDTH), -50]
    if edge == 'bottom':
        return [random.randint(0, WIDTH), +50]
    if edge == 'left':
        return [-50, random.randint(0, HEIGHT)]
    if edge == 'right':
        return [WIDTH +50, random.randint(0, HEIGHT)]



# Function to calculate direction
def get_direction(source, target):
    dx = target[0] - source[0]
    dy = target[1] - source[1]
    dist = math.hypot(dx, dy)
    if dist == 0:
        return 0, 0
    return dx / dist, dy / dist

# Main Loop
running = True
while running:
    clock.tick(60)
    win.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Fire Bullet
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shoot_sound.play()
                bullet_dir = get_direction(player_pos, pygame.mouse.get_pos())
                bullet = {
                    "pos": [player_pos[0] + 20, player_pos[1] + 20],
                    "dir": bullet_dir
                }
                bullets.append(bullet)



    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT]:
            player_pos[0] += player_speed
        if keys[pygame.K_UP]:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN]:
            player_pos[1] += player_speed

        # Zombie spawn logic
        zombie_spawn_timer += 1
        if zombie_spawn_timer >= 90:
            zombies.append({"pos" : spawn_zombie(), "last_attack": 0})
            zombie_spawn_timer = 0

        # Move zombies toward player
        for zombie in zombies:
            zx, zy = zombie["pos"]
            dx, dy = get_direction([zx, zy], player_pos)
            zombie["pos"][0] += dx * zombie_speed
            zombie["pos"][1] += dy * zombie_speed

        # Move bullets
        for bullet in bullets:
            bullet["pos"][0] += bullet["dir"][0] * bullet_speed
            bullet["pos"][1] += bullet["dir"][1] * bullet_speed

        # Remove off-screen bullets
        bullets = [b for b in bullets if 0 <= b["pos"][0] <= WIDTH and 0 <= b["pos"][1] <= HEIGHT]

        # Collision: Bullet hits zombie
        for bullet in bullets[:]:
            for zombie in zombies[:]:
                bx, by = bullet["pos"]
                zx, zy = zombie["pos"]
                if abs(bx - zx) < 30 and abs(by - zy) < 30:
                    zombie_hit_sound.play()
                    splatters.append((zx + 25, zy + 25, time.time()))
                    bullets.remove(bullet)
                    zombies.remove(zombie)
                    score += 1
                    break

        # Check for zombie-player collision

        current_time = time.time()
        player_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 50)

        for zombie in zombies:
            zombie_rect = pygame.Rect(zombie["pos"][0], zombie["pos"][1], 50, 50)
            if player_rect.colliderect(zombie_rect):
                if current_time - zombie["last_attack"] > 0.8:  # cooldown in seconds
                    player_health -= 10
                    zombie["last_attack"] = current_time
                    player_hit_sound.play()

        if player_health <= 0 and not game_over:
            game_over_sound.play()
            game_over = True

    # Draw player, zombie, bullets
    win.blit(PLAYER_IMAGE, player_pos)

    for zombie in zombies:
        win.blit(ZOMBIE_IMAGE, zombie["pos"])

    for bullet in bullets:
        win.blit(BULLET_IMAGE, bullet["pos"])

    # Draw Score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(score_text, (10, 10))

    # Draw Health Bar
    pygame.draw.rect(win, (255, 0, 0), (10, 50, 200, 20))
    pygame.draw.rect(win, (0, 255, 0), (10, 50, max(0, int(2 * player_health)), 20))
    health_text = font.render(f"Health: {int(player_health)}", True, (255, 255, 255))
    win.blit(health_text, (220, 48))

    # Game Over screen
    if game_over:
        over_text = big_font.render("GAME OVER", True, (255, 50, 50))
        win.blit(over_text, (WIDTH // 2 - 160, HEIGHT // 2 - 40))
        retry_text = font.render("Press R to Restart or ESC to Quit", True, (200, 200, 200))
        win.blit(retry_text, (WIDTH // 2 - 180, HEIGHT // 2 + 30))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset game
            pygame.mouse.set_pos(WIDTH // 2, HEIGHT // 2)
            player_pos = [WIDTH // 2, HEIGHT // 2]
            player_health = 100
            score = 0
            zombies.clear()
            bullets.clear()
            game_over = False
        elif keys[pygame.K_ESCAPE]:
            running = False

    # Draw blood splatters
    for splatter in splatters[:]:
        x,y,t = splatter
        if time.time() - t < 1.0:
            pygame.draw.circle(win, (139, 0, 0), (int(x), int(y)), 25)
        else:
            splatters.remove(splatter)



    pygame.display.update()

pygame.quit()
sys.exit()
