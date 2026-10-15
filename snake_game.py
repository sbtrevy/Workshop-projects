
import pygame
import random

# Initialize pygame
pygame.init()

# Create the game window
WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Snake Game")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Game settings
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
small_font = pygame.font.SysFont(None, 24)

# Difficulty controls how many times the snake moves each second.
LEVELS = {
    pygame.K_1: ("Easy", 6),
    pygame.K_2: ("Medium", 10),
    pygame.K_3: ("Hard", 15),
}

# Starting snake and fruit
snake = [(100, 100), (80, 100), (60, 100)]
direction = (CELL_SIZE, 0)

fruit = (
    random.randrange(0, WIDTH, CELL_SIZE),
    random.randrange(0, HEIGHT, CELL_SIZE)
)

score = 0
running = True
game_over = False
level_name = None
game_speed = 0

# Main game loop
while running:

    # Handle keyboard input
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Choose a difficulty before the first round.
            if level_name is None:
                if event.key in LEVELS:
                    level_name, game_speed = LEVELS[event.key]
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    running = False
                continue

            if game_over:
                if event.key == pygame.K_r:
                    # Start a fresh round.
                    snake = [(100, 100), (80, 100), (60, 100)]
                    direction = (CELL_SIZE, 0)
                    score = 0
                    fruit = (
                        random.randrange(0, WIDTH, CELL_SIZE),
                        random.randrange(0, HEIGHT, CELL_SIZE)
                    )
                    game_over = False
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    running = False
                continue

            if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                direction = (0, -CELL_SIZE)

            elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                direction = (0, CELL_SIZE)

            elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                direction = (-CELL_SIZE, 0)

            elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                direction = (CELL_SIZE, 0)

    if not game_over and level_name is not None:

        # Move the snake
        head_x, head_y = snake[0]
        new_head = (
            head_x + direction[0],
            head_y + direction[1]
        )

        # Check whether the snake eats the fruit
        ate_fruit = new_head == fruit

        # Check collisions with the walls
        if (
            new_head[0] < 0 or new_head[0] >= WIDTH
            or new_head[1] < 0 or new_head[1] >= HEIGHT
        ):
            game_over = True

        # Check collision with the snake's body
        body_to_check = snake if ate_fruit else snake[:-1]

        if new_head in body_to_check:
            game_over = True

        if not game_over:

            snake.insert(0, new_head)

            if ate_fruit:
                score += 1

                # Generate a new fruit outside the snake
                empty_cells = [
                    (x, y)
                    for x in range(0, WIDTH, CELL_SIZE)
                    for y in range(0, HEIGHT, CELL_SIZE)
                    if (x, y) not in snake
                ]

                if empty_cells:
                    fruit = random.choice(empty_cells)
                else:
                    game_over = True

            else:
                snake.pop()

    # Draw the game
    screen.fill(BLACK)

    # Draw the fruit
    pygame.draw.rect(
        screen, RED,
        (fruit[0], fruit[1], CELL_SIZE, CELL_SIZE)
    )

    # Draw the snake
    for segment in snake:
        pygame.draw.rect(
            screen, GREEN,
            (segment[0], segment[1], CELL_SIZE, CELL_SIZE)
        )

    # Display the score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    if level_name is not None:
        level_text = small_font.render(f"Level: {level_name}", True, WHITE)
        screen.blit(level_text, (10, 38))

    if level_name is None:
        prompt = font.render("Choose a level: 1 Easy  2 Medium  3 Hard", True, WHITE)
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2))

    # Display game-over message
    if game_over:
        message = font.render(
            "GAME OVER! Press R to retry or Q to quit.",
            True, WHITE
        )
        screen.blit(
            message,
            (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2)
        )

    pygame.display.update()

    # Control game speed
    clock.tick(game_speed if game_speed else 10)

pygame.quit()
