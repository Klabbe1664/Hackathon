import pygame
import random

pygame.init()

# display
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

#Background
background_image = pygame.image.load('background.png').convert()
bg_width = background_image.get_width()
bg_x1 = 0
bg_x2 = bg_width

# Birds
bird_images = ['bird1.png', 'bird2.png', 'bird3.png', 'bird4.png']
menu_birds = [pygame.transform.scale(pygame.image.load(img).convert_alpha(), (100, 70)) for img in bird_images]
game_birds = [pygame.transform.scale(pygame.image.load(img).convert_alpha(), (50, 35)) for img in bird_images]

# High score
high_score = 0

# Bar obstacles 
class Obstacle:
    def __init__(self, x, height, gap):
        self.x = x
        self.top_height = height
        self.bottom_height = SCREEN_HEIGHT - (height + gap)
        self.width = 80
        self.color = (113, 204, 46)
        self.gap = gap
        self.top_rect = pygame.Rect(x, 0, self.width, self.top_height)
        self.bottom_rect = pygame.Rect(x, SCREEN_HEIGHT - self.bottom_height, self.width, self.bottom_height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.top_rect)
        pygame.draw.rect(screen, self.color, self.bottom_rect)

    def update(self):
        self.x -= 2
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def off_screen(self):
        return self.x < -self.width

    def collide(self, rect):
        return self.top_rect.colliderect(rect) or self.bottom_rect.colliderect(rect)

#  Menu Bird Selection
def draw_menu(selected_index, high_score):
    screen.fill((150, 150, 150))
    menu_text = font.render('Choose a Bird', True, (0, 0, 0))
    high_score_text = font.render(f'High Score: {high_score}', True, (255, 255, 255))
    screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 50))
    screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 100))
    
    bird_names = ["Blocket Bird", "Nybegagnat Bird", "Finn Bird", "Nybrukt Bird"]  
    
    for i, bird in enumerate(menu_birds):
        x = 100 + i * (SCREEN_WIDTH // len(menu_birds))
        y = 200
        screen.blit(bird, (x, y))
        if i == selected_index:
            pygame.draw.rect(screen, (255, 0, 0), (x - 5, y - 5, bird.get_width() + 10, bird.get_height() + 10), 2)
        
        #Name of each bird below its image
        bird_text = font.render(bird_names[i], True, (0, 0, 0))
        text_x = x + (bird.get_width() / 2) - (bird_text.get_width() / 2)
        text_y = y + bird.get_height() + 5
        screen.blit(bird_text, (text_x, text_y))
    
    pygame.display.update()


# Main game logic
def main_game(selected_bird_index):
    global high_score
    selected_bird = game_birds[selected_bird_index]
    bird_rect = selected_bird.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    bird_y_velocity = 0
    gravity = 0.5
    flap_power = -10
    ground_y = SCREEN_HEIGHT - 40
    bg_scroll_speed = -2
    bg_x1 = 0
    bg_x2 = bg_width
    obstacles = []
    OBSTACLE_GAP = 200
    OBSTACLE_FREQUENCY = 120
    frame_count = 0
    score = 0
    passed_obstacles = []
    game_started = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    bird_y_velocity = flap_power
                    if not game_started:
                        game_started = True  # Start the game on first W

        if not game_started:
            screen.fill((0, 0, 0))
            screen.blit(background_image, (bg_x1, 0))
            screen.blit(background_image, (bg_x2, 0))
            screen.blit(selected_bird, bird_rect)
            start_text = font.render("Press W  -  :)  GL HF", True, (0, 0, 0))
            screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        else:
            bird_y_velocity += gravity
            bird_rect.y += int(bird_y_velocity)

            bg_x1 += bg_scroll_speed
            bg_x2 += bg_scroll_speed
            if bg_x1 <= -bg_width:
                bg_x1 = bg_width
            if bg_x2 <= -bg_width:
                bg_x2 = bg_width

            screen.fill((0, 0, 0))
            screen.blit(background_image, (bg_x1, 0))
            screen.blit(background_image, (bg_x2, 0))
            screen.blit(selected_bird, bird_rect)

            frame_count += 1
            if frame_count % OBSTACLE_FREQUENCY == 0:
                obstacle_height = random.randint(100, SCREEN_HEIGHT - OBSTACLE_GAP - 100)
                new_obstacle = Obstacle(SCREEN_WIDTH, obstacle_height, OBSTACLE_GAP)
                obstacles.append(new_obstacle)
                passed_obstacles.append(False)

            for index, obstacle in enumerate(obstacles):
                obstacle.update()
                obstacle.draw(screen)
                if obstacle.collide(bird_rect):
                    if score > high_score:
                        high_score = score
                    running = False
                if obstacle.x + obstacle.width < bird_rect.centerx and not passed_obstacles[index]:
                    score += 1
                    passed_obstacles[index] = True

            if bird_rect.bottom >= ground_y or bird_rect.top <= 0:
                if score > high_score:
                    high_score = score
                running = False

            score_text = font.render(f'Score: {score}', True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(60)

    return high_score

# Restart game to main menu after death
selected_index = 0
while True:
    draw_menu(selected_index, high_score)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                selected_index = (selected_index - 1) % len(menu_birds)
            elif event.key == pygame.K_RIGHT:
                selected_index = (selected_index + 1) % len(menu_birds)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                high_score = main_game(selected_index)

