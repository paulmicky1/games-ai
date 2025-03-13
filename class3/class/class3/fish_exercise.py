import pygame
import random
import math

# Screen Constants
WIDTH, HEIGHT = 512, 512
NUM_FISH = 50  # Number of fish in the school
BUBBLE_COUNT = 20  # Number of bubbles in the scene
MAX_SPEED = 2.5  # Speed limit for fish movement
NEIGHBOR_RADIUS = 50  # Perception radius for alignment & cohesion
SEPARATION_RADIUS = 25  # Distance to maintain from other fish

# Boid Behavior Strengths
SEPARATION_FORCE = 1.2  # Avoid crowding
ALIGNMENT_FORCE = 0.1  # Match velocity
COHESION_FORCE = 0.05  # Stay with the group

# Background Colors
BG_TOP = (10, 50, 120)
BG_BOTTOM = (0, 20, 40)

class Fish:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.vx = random.uniform(-MAX_SPEED, MAX_SPEED)
        self.vy = random.uniform(-MAX_SPEED, MAX_SPEED)
        self.color = (random.randint(100, 255), random.randint(50, 200), random.randint(100, 255))
    
    def update(self, flock):
        separation = self.separate(flock)
        alignment = self.align(flock)
        cohesion = self.cohere(flock)

        # Apply the three boid rules
        self.vx += separation[0] * SEPARATION_FORCE + alignment[0] * ALIGNMENT_FORCE + cohesion[0] * COHESION_FORCE
        self.vy += separation[1] * SEPARATION_FORCE + alignment[1] * ALIGNMENT_FORCE + cohesion[1] * COHESION_FORCE

        # Limit speed
        speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
        if speed > MAX_SPEED:
            scale = MAX_SPEED / speed
            self.vx *= scale
            self.vy *= scale

        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Wrap-around behavior (if a fish exits one side, it enters from the other)
        self.x %= WIDTH
        self.y %= HEIGHT

    def separate(self, flock):
        separation_vector = [0, 0]
        for other in flock:
            if other != self:
                distance = math.hypot(self.x - other.x, self.y - other.y)
                if distance < SEPARATION_RADIUS and distance > 0:
                    separation_vector[0] += (self.x - other.x) / distance
                    separation_vector[1] += (self.y - other.y) / distance
        return separation_vector

    def align(self, flock):
        avg_vx, avg_vy = 0, 0
        count = 0
        for other in flock:
            if other != self:
                distance = math.hypot(self.x - other.x, self.y - other.y)
                if distance < NEIGHBOR_RADIUS:
                    avg_vx += other.vx
                    avg_vy += other.vy
                    count += 1
        if count > 0:
            avg_vx /= count
            avg_vy /= count
            return [avg_vx - self.vx, avg_vy - self.vy]
        return [0, 0]
    
    def cohere(self, flock):
        center_x, center_y = 0, 0
        count = 0
        for other in flock:
            if other != self:
                distance = math.hypot(self.x - other.x, self.y - other.y)
                if distance < NEIGHBOR_RADIUS:
                    center_x += other.x
                    center_y += other.y
                    count += 1
        if count > 0:
            center_x /= count
            center_y /= count
            return [(center_x - self.x), (center_y - self.y)]
        return [0, 0]
    
    def draw(self, screen):
        angle = math.atan2(self.vy, self.vx)
        pygame.draw.polygon(screen, self.color, [
            (self.x + math.cos(angle) * 10, self.y + math.sin(angle) * 10),
            (self.x + math.cos(angle + 5 * math.pi / 6) * 10, self.y + math.sin(angle + 5 * math.pi / 6) * 10),
            (self.x + math.cos(angle - 5 * math.pi / 6) * 10, self.y + math.sin(angle - 5 * math.pi / 6) * 10)
        ])

class Bubble:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(HEIGHT - 10, HEIGHT)
        self.radius = random.randint(2, 6)
        self.speed = random.uniform(0.5, 1.5)
    
    def update(self):
        self.y -= self.speed
        if self.y < 0:
            self.y = HEIGHT
            self.x = random.randint(0, WIDTH)
    
    def draw(self, screen):
        pygame.draw.circle(screen, (200, 200, 255), (self.x, int(self.y)), self.radius)

def draw_background(screen):
    for y in range(HEIGHT):
        color = [int(BG_TOP[i] + (BG_BOTTOM[i] - BG_TOP[i]) * (y / HEIGHT)) for i in range(3)]
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fish Simulation")
    clock = pygame.time.Clock()

    fish = [Fish() for _ in range(NUM_FISH)]
    bubbles = [Bubble() for _ in range(BUBBLE_COUNT)]
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        for f in fish:
            f.update(fish)
        for bubble in bubbles:
            bubble.update()
        
        draw_background(screen)
        for bubble in bubbles:
            bubble.draw(screen)
        for f in fish:
            f.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    
if __name__ == "__main__":
    main()