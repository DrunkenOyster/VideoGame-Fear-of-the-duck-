#   png branch
import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Game window dimensions
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fear of the Duck")

# Font for text
font = pygame.font.SysFont(None, 36)
welcome_font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 24)

# Welcome screen function
def welcome_screen():
    window.fill((144, 238, 144))  # Light green background
    title_text = welcome_font.render("Fear of the Duck", True, (0, 0, 0))
    subtitle_text = small_font.render("Are you ready to run away from the mighty duck?", True, (0, 0, 0))
    start_text = font.render("Click here to start the game", True, (0, 0, 0))
    window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
    window.blit(subtitle_text, (WIDTH // 2 - subtitle_text.get_width() // 2, HEIGHT // 3 + 50))
    window.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

# Class for the player (child)
class Player(pygame.sprite.Sprite):
    def __init__(self, speed=5):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0,90, 0))  # Green color for the player
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 75)
        self.speed = speed
        self.lives = 3

    def update(self, keys_pressed):
        old_x, old_y = self.rect.x, self.rect.y
        if keys_pressed[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys_pressed[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys_pressed[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if pygame.sprite.spritecollide(self, obstacles, False):
            self.rect.x, self.rect.y = old_x, old_y

# Class for the duck
class Duck(pygame.sprite.Sprite):
    def __init__(self, speed=2, size=(50, 50)):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill((255, 255, 0))  # Yellow color for the duck
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, 50)
        self.base_speed = speed
        self.slow_speed = 1

    def update(self, player_pos):
        speed = self.slow_speed if pygame.sprite.spritecollide(self, obstacles, False) else self.base_speed
        if self.rect.x < player_pos[0]:
            self.rect.x += speed
        elif self.rect.x > player_pos[0]:
            self.rect.x -= speed
        if self.rect.y < player_pos[1]:
            self.rect.y += speed
        elif self.rect.y > player_pos[1]:
            self.rect.y -= speed

# Class for obstacles
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((random.randint(50, 100), 20))
        self.image.fill((128, 128, 128))  # Gray color
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(100, HEIGHT - 150)

# Sprite groups
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

def reset_level(player_speed=5, duck_speed=2, duck_size=(50, 50)):
    all_sprites.empty()
    obstacles.empty()
    player = Player(speed=player_speed)
    duck = Duck(speed=duck_speed, size=duck_size)
    all_sprites.add(player)
    all_sprites.add(duck)
    for _ in range(5):
        obstacle = Obstacle()
        obstacles.add(obstacle)
        all_sprites.add(obstacle)
    return player, duck

# Main game loop
def game_loop():
    level = 1
    player, duck = reset_level()
    timer_start = time.time()
    clock = pygame.time.Clock()
    winner = False

    running = True
    while running:
        clock.tick(60)
        elapsed_time = time.time() - timer_start

        # Check level progress
        if elapsed_time >= 60:  # Check if one minute has passed
            level += 1
            if level == 2:
                player, duck = reset_level(player_speed=5, duck_speed=3)  # Duck speed at 3 for level 2
            elif level == 3:
                player, duck = reset_level(player_speed=5, duck_speed=3, duck_size=(60, 60))  # Duck speed at 3, larger size for level 3
            else:
                print("You won!")
                winner = True
                break

            timer_start = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys_pressed = pygame.key.get_pressed()
        player.update(keys_pressed)
        duck.update(player.rect.center)

        if pygame.sprite.collide_rect(player, duck):
            player.lives -= 1
            player.rect.center = (WIDTH // 2, HEIGHT - 75)
            if player.lives <= 0:
                running = False

        window.fill((144, 238, 144))  # Light green background
        all_sprites.draw(window)

        # Display lives and level
        lives_text = font.render(f"Lives: {player.lives}", True, (0, 0, 0))
        level_text = font.render(f"Level: {level}", True, (0, 0, 0))
        timer_text = font.render(f"Time: {int(60 - elapsed_time)}", True, (0, 0, 0))
        window.blit(lives_text, (10, 10))
        window.blit(level_text, (10, 40))
        window.blit(timer_text, (10, 70))

        pygame.display.flip()

    # Game Over: Ask if the player wants to restart
    game_over_screen(winner)


def game_over_screen(result):
    window.fill((144, 238, 144))
    if result:
        game_over_text = welcome_font.render("You won!", True, (0, 100, 0))
    else:
        game_over_text = welcome_font.render("Game Over", True, (255, 0, 0))
    retry_text = font.render("Do you want to try again? (Y/N)", True, (0, 0, 0))
    window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    window.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    waiting = False
                    game_loop()  # Restart the game
                elif event.key == pygame.K_n:
                    print("Good bye")
                    pygame.display.quit() 
                    pygame.quit()  
                    sys.exit()

# Display the welcome screen
welcome_screen()

# Start the game
game_loop()
