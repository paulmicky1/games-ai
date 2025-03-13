import pygame as pg
import random

# Initialize pygame
pg.init()

# Game settings
w, h = 12, 8  # Board dimensions (tiles)
L = 50  # Tile size in pixels
pad = 5  # Padding
toppad = 30  # Space at the top for text
speed = 200  # Snake speed (milliseconds per move)

# Colors
BACKGROUND = (0, 0, 0)
GRID_COLOR = (50, 50, 50)
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
TEXT_COLOR = (220, 220, 220)

# Set up the screen
screen = pg.display.set_mode((w * L, h * L + toppad))
pg.display.set_caption("Snake Game")

# Load font
default_font = pg.font.SysFont(pg.font.get_default_font(), 30)

# Snake setup
snake = [(h // 2, w // 2)]
direction = "UP"

# Function to generate food farthest from the snake
def get_farthest_food():
    max_distance = -1
    best_pos = None
    for row in range(h):
        for col in range(w):
            if (row, col) not in snake:
                # Find the max distance from any snake part
                min_dist = min(abs(row - s[0]) + abs(col - s[1]) for s in snake)
                if min_dist > max_distance:
                    max_distance = min_dist
                    best_pos = (row, col)
    return best_pos

# Initial food position
food_pos = get_farthest_food()

running = True
paused = False  # Pause when space is pressed
clock = pg.time.Clock()

while running:
    screen.fill(BACKGROUND)

    # Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE or event.key == pg.K_SPACE:
                running = False
            elif event.key == pg.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pg.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pg.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pg.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    if not paused:
        # Update snake position
        head_row, head_col = snake[0]

        if direction == "UP":
            new_head = ((head_row - 1) % h, head_col)  # Wrap at top/bottom
        elif direction == "RIGHT":
            new_head = (head_row, (head_col + 1) % w)  # Wrap at left/right
        elif direction == "DOWN":
            new_head = ((head_row + 1) % h, head_col)
        elif direction == "LEFT":
            new_head = (head_row, (head_col - 1) % w)

        # Check for self-collision (Game Over)
        if new_head in snake:
            print("Game Over!")
            running = False

        # Add new head to snake
        snake.insert(0, new_head)

        # Check if snake eats food
        if new_head == food_pos:
            food_pos = get_farthest_food()  # Move food as far as possible
            speed = max(50, speed - 10)  # Increase speed over time
        else:
            snake.pop()  # Remove last tail segment

    # Draw game board
    for col in range(w):
        for row in range(h):
            pg.draw.rect(screen, GRID_COLOR, pg.Rect(col * L + pad, row * L + pad + toppad, L - pad, L - pad))

    # Draw snake
    for row, col in snake:
        pg.draw.rect(screen, SNAKE_COLOR, pg.Rect(col * L + pad, row * L + pad + toppad, L - pad, L - pad))

    # Draw food
    pg.draw.rect(screen, FOOD_COLOR, pg.Rect(food_pos[1] * L + pad, food_pos[0] * L + pad + toppad, L - pad, L - pad))

    # Display text
    text = default_font.render(f'Score: {len(snake) - 1}', True, TEXT_COLOR)
    screen.blit(text, (5, 5))

    pg.display.flip()
    pg.time.delay(speed)  # Control game speed

pg.quit()
