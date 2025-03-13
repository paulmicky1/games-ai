import pygame
import random
import math

# Constants
WIDTH, HEIGHT = 512, 512
NUM_FISH = 50  # Increased to 50, more fish means more complex behavior
MAX_SPEED = 2  # Controls the max speed of fish movement
NEIGHBOR_RADIUS = 50  # Distance to consider other fish as neighbors
SEPARATION_RADIUS = 30  # Distance to keep from other fish (avoid crowding)
SEPARATION_FORCE = 0.8  # Higher value = fish separate more aggressively
ALIGNMENT_FORCE = 0.1  # Higher value = fish align their direction more
COHESION_FORCE = 0.05  # Higher value = fish stay closer together
BG_COLOR_TOP = (10, 50, 100)  # Water gradient (top color)
BG_COLOR_BOTTOM = (0, 10, 30)  # Water gradient (bottom color)
FISH_COLOR = (255, 100, 200)
BUBBLE_COUNT = 20

class Fish:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = [random.randint(100, 255), random.randint(50, 200), random.randint(100, 255)]
    
    def update(self, flock):
        separation = self.separate(flock)  # Rule 1: Avoid crowding
        alignment = self.align(flock)  # Rule 2: Align with nearby fish
        cohesion = self.cohere(flock)  # Rule 3: Move toward the center
        
        self.vx += separation[0] * SEPARATION_FORCE + alignment[0] * ALIGNMENT_FORCE + cohesion[0] * COHESION_FORCE
        self.vy += separation[1] * SEPARATION_FORCE + alignment[1] * ALIGNMENT_FORCE + cohesion[1] * COHESION_FORCE
        
        speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
        if speed > MAX_SPEED:
            scale_factor = MAX_SPEED / speed
            self.vx *= scale_factor
            self.vy *= scale_factor
        
        self.x += self.vx
        self.y += self.vy
        
        # Wrap around screen (fish reappear on opposite side)
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = HEIGHT
        elif self.y > HEIGHT:
            self.y = 0
        
        # Add slight randomness to movement
        self.vx += random.uniform(-0.05, 0.05)
        self.vy += random.uniform(-0.05, 0.05)
    
    def separate(self, flock):
        # Avoid getting too close to other fish
        separation_vector = [0, 0]
        for other_fish in flock:
            if other_fish != self:
                distance = math.sqrt((self.x - other_fish.x) ** 2 + (self.y - other_fish.y) ** 2)
                if distance < SEPARATION_RADIUS:
                    separation_vector[0] += (self.x - other_fish.x) / distance
                    separation_vector[1] += (self.y - other_fish.y) / distance
        return separation_vector
    
    def align(self, flock):
        # Align fish movement with nearby fish
        avg_velocity = [0, 0]
        num_neighbors = 0
        for other_fish in flock:
            if other_fish != self:
                distance = math.sqrt((self.x - other_fish.x) ** 2 + (self.y - other_fish.y) ** 2)
                if distance < NEIGHBOR_RADIUS:
                    avg_velocity[0] += other_fish.vx
                    avg_velocity[1] += other_fish.vy
                    num_neighbors += 1
        if num_neighbors > 0:
            avg_velocity[0] /= num_neighbors
            avg_velocity[1] /= num_neighbors
            return [avg_velocity[0] - self.vx, avg_velocity[1] - self.vy]
        return [0, 0]
    
    def cohere(self, flock):
        # Move towards the average position of nearby fish
        center_of_mass = [0, 0]
        num_neighbors = 0
        for other_fish in flock:
            if other_fish != self:
                distance = math.sqrt((self.x - other_fish.x) ** 2 + (self.y - other_fish.y) ** 2)
                if distance < NEIGHBOR_RADIUS:
                    center_of_mass[0] += other_fish.x
                    center_of_mass[1] += other_fish.y
                    num_neighbors += 1
        if num_neighbors > 0:
            center_of_mass[0] /= num_neighbors
            center_of_mass[1] /= num_neighbors
            return [center_of_mass[0] - self.x, center_of_mass[1] - self.y]
        return [0, 0]
    
    def draw(self, screen):
        angle = math.atan2(self.vy, self.vx)
        pygame.draw.polygon(screen, self.color, [
            (self.x + math.cos(angle) * 10, self.y + math.sin(angle) * 10),
            (self.x + math.cos(angle + 5 * math.pi / 6) * 10, self.y + math.sin(angle + 5 * math.pi / 6) * 10),
            (self.x + math.cos(angle - 5 * math.pi / 6) * 10, self.y + math.sin(angle - 5 * math.pi / 6) * 10)
        ])

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Boids Simulation")
    clock = pygame.time.Clock()
    
    fish = [Fish(random.randint(0, WIDTH), random.randint(0, HEIGHT),
                 random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(NUM_FISH)]
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        for fishy in fish:
            fishy.update(fish)
        
        for y in range(HEIGHT):
            color = [int(BG_COLOR_TOP[i] + (BG_COLOR_BOTTOM[i] - BG_COLOR_TOP[i]) * (y / HEIGHT)) for i in range(3)]
            pygame.draw.line(screen, color, (0, y), (WIDTH, y))
        
        for fishy in fish:
            fishy.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    
if __name__ == "__main__":
    main()
