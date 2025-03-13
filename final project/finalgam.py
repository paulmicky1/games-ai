import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
PLAYER_SIZE = 50
ENEMY_SIZE = 50
BULLET_SIZE = 10
PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 2
GRAVITY = 0.5
JUMP_STRENGTH = -10
PLATFORM_HEIGHT = 20

# Load assets
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (PLAYER_SIZE, PLAYER_SIZE))
enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_SIZE, ENEMY_SIZE))
bullet_img = pygame.image.load("bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (BULLET_SIZE, BULLET_SIZE))
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
shoot_sound = pygame.mixer.Sound("bullet_sound.wav")

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Game with Jumping, Platforms, and Assets")

# Player, enemies, bullets, platforms
player = pygame.Rect(100, HEIGHT - PLAYER_SIZE - 10, PLAYER_SIZE, PLAYER_SIZE)
enemies = []
bullets = []
platforms = [pygame.Rect(150, 400, 200, PLATFORM_HEIGHT), pygame.Rect(400, 300, 200, PLATFORM_HEIGHT)]

player_vel_y = 0
on_ground = False
bg_x = 0

def create_enemy():
    x_pos = random.randint(WIDTH, WIDTH + 200)
    enemies.append(pygame.Rect(x_pos, HEIGHT - ENEMY_SIZE - 10, ENEMY_SIZE, ENEMY_SIZE))

# Game loop
running = True
clock = pygame.time.Clock()
score = 0

while running:
    screen.blit(background, (bg_x, 0))
    screen.blit(background, (bg_x + WIDTH, 0))
    bg_x -= 2
    if bg_x <= -WIDTH:
        bg_x = 0
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Shoot bullet
                bullets.append(pygame.Rect(player.x + PLAYER_SIZE // 2, player.y, BULLET_SIZE, BULLET_SIZE))
                shoot_sound.play()
            if event.key == pygame.K_UP and on_ground:  # Jump
                player_vel_y = JUMP_STRENGTH
                on_ground = False
    
    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player.x < WIDTH - PLAYER_SIZE:
        player.x += PLAYER_SPEED
    
    # Apply gravity
    player_vel_y += GRAVITY
    player.y += player_vel_y
    
    # Collision with ground
    if player.y >= HEIGHT - PLAYER_SIZE - 10:
        player.y = HEIGHT - PLAYER_SIZE - 10
        player_vel_y = 0
        on_ground = True
    
    # Collision with platforms
    for platform in platforms:
        if player.colliderect(platform) and player_vel_y > 0:
            player.y = platform.y - PLAYER_SIZE
            player_vel_y = 0
            on_ground = True
    
    # Enemy movement
    if random.randint(1, 50) == 1:
        create_enemy()
    for enemy in enemies[:]:
        enemy.x -= ENEMY_SPEED
        if enemy.x < 0:
            enemies.remove(enemy)
    
    # Bullet movement
    for bullet in bullets[:]:
        bullet.y -= BULLET_SPEED
        if bullet.y < 0:
            bullets.remove(bullet)
    
    # Collision detection
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                break
    
    # Draw elements
    screen.blit(player_img, (player.x, player.y))
    for enemy in enemies:
        screen.blit(enemy_img, (enemy.x, enemy.y))
    for bullet in bullets:
        screen.blit(bullet_img, (bullet.x, bullet.y))
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)
    
    # Show score
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))
    
    pygame.display.update()
    clock.tick(30)

pygame.quit()
