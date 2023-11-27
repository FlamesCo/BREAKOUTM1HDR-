import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BRICK_COLOR = (255, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

paddle_width = 100
paddle_height = 20
paddle_speed = 10

paddle_x = SCREEN_WIDTH / 2 - paddle_width / 2
paddle_y = SCREEN_HEIGHT - 50

ball_radius = 10
ball_x = SCREEN_WIDTH / 2
ball_y = paddle_y - ball_radius

ball_speed_x = 5
ball_speed_y = -5

# Bricks
brick_width = 80
brick_height = 30
bricks = []

for row in range(4):
    for col in range(10):
        brick = pygame.Rect(col * brick_width, row * brick_height + 100, brick_width, brick_height)
        bricks.append(brick)

# Fonts
font = pygame.font.Font(None, 36)

# Game states
PLAYING = 0
GAME_OVER = 1
WIN = 2
game_state = PLAYING

def restart_game():
    global paddle_x, ball_x, ball_y, ball_speed_x, ball_speed_y, bricks, game_state
    paddle_x = SCREEN_WIDTH / 2 - paddle_width / 2
    ball_x = SCREEN_WIDTH / 2
    ball_y = paddle_y - ball_radius
    ball_speed_x = 5
    ball_speed_y = -5
    bricks = []
    for row in range(4):
        for col in range(10):
            brick = pygame.Rect(col * brick_width, row * brick_height + 100, brick_width, brick_height)
            bricks.append(brick)
    game_state = PLAYING

# Main loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_state == PLAYING:
        # Input handling
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            paddle_x = max(0, paddle_x - paddle_speed)
        if keys_pressed[pygame.K_RIGHT]:
            paddle_x = min(SCREEN_WIDTH - paddle_width, paddle_x + paddle_speed)

        # Ball movement
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Ball collisions with walls
        if ball_x <= 0 or ball_x >= SCREEN_WIDTH:
            ball_speed_x = -ball_speed_x
        if ball_y <= 0:
            ball_speed_y = -ball_speed_y

        # Ball collision with paddle
        if ball_y >= paddle_y - ball_radius and \
           paddle_x <= ball_x <= paddle_x + paddle_width:
            ball_speed_y = -ball_speed_y

        # Ball collision with bricks
        for brick in bricks:
            if brick.colliderect(pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, 2 * ball_radius, 2 * ball_radius)):
                bricks.remove(brick)
                ball_speed_y = -ball_speed_y

        # Check for game over
        if ball_y >= SCREEN_HEIGHT:
            game_state = GAME_OVER

        # Check for win
        if len(bricks) == 0:
            game_state = WIN

    # Drawing
    screen.fill((0, 0, 0))

    if game_state == PLAYING:
        # Draw bricks
        for brick in bricks:
            pygame.draw.rect(screen, BRICK_COLOR, brick)

        pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), ball_radius)
        pygame.draw.rect(screen, WHITE, (int(paddle_x), int(paddle_y), paddle_width, paddle_height))
    elif game_state == GAME_OVER:
        text = font.render("Game Over. Press R to restart.", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    elif game_state == WIN:
        text = font.render("You Win! Press R to restart.", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

    pygame.display.flip()
    clock.tick(FPS)

    # Restart game if 'R' key is pressed
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_r]:
        restart_game()
