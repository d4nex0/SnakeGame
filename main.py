import pygame
import random
import sys

# Инициализация pygame
pygame.init()

# Константы
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 20
DEFAULT_SPEED = 15

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)


# Создание окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Змейка с препятствиями')
clock = pygame.time.Clock()



class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class Settings:
    def __init__(self):
        self.speed = DEFAULT_SPEED
        self.obstacle_frequency = 5


class Menu:
    def __init__(self):
        self.settings = Settings()
        center_x = WINDOW_WIDTH // 2
        self.play_button = Button(center_x - 100, 200, 200, 50, "Играть", GREEN)
        self.settings_button = Button(center_x - 100, 300, 200, 50, "Настройки", BLUE)
        self.exit_button = Button(center_x - 100, 400, 200, 50, "Выход", RED)
        self.upravlenie_button = Button(center_x - 100, 400, 200, 50, "Собирайте еду и избегайте препятствий!", BLACK)


        # Кнопки настроек
        self.speed_up = Button(center_x + 50, 200, 30, 30, "+", GREEN)
        self.speed_down = Button(center_x - 80, 200, 30, 30, "-", RED)
        self.back_button = Button(center_x - 100, 500, 200, 50, "Назад", GRAY)

    def draw_main_menu(self, surface):
        surface.fill(BLACK)
        self.play_button.draw(surface)
        self.settings_button.draw(surface)
        self.exit_button.draw(surface)
        self.upravlenie_button.draw(surface)
        pygame.display.flip()

    def draw_settings_menu(self, surface):
        surface.fill(BLACK)
        font = pygame.font.Font(None, 36)


        speed_text = font.render(f"Скорость: {self.settings.speed}", True, WHITE)
        surface.blit(speed_text, (WINDOW_WIDTH//2 - 60, 150))

        self.speed_up.draw(surface)
        self.speed_down.draw(surface)
        self.back_button.draw(surface)
        pygame.display.flip()


class Snake:
    def __init__(self):
        self.positions = [(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)]
        self.direction = "RIGHT"
        self.length = 1

    def move(self):
        x, y = self.positions[0]
        if self.direction == "UP":
            y -= BLOCK_SIZE
        elif self.direction == "DOWN":
            y += BLOCK_SIZE
        elif self.direction == "LEFT":
            x -= BLOCK_SIZE
        elif self.direction == "RIGHT":
            x += BLOCK_SIZE

        new_head = (x, y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def grow(self):
        self.length += 1

    def check_collision(self):
        head = self.positions[0]
        if (head[0] < 0 or head[0] >= WINDOW_WIDTH or
                head[1] < 0 or head[1] >= WINDOW_HEIGHT):
            return True
        if head in self.positions[1:]:
            return True
        return False


class Game:
    def __init__(self, settings):
        self.settings = settings
        self.snake = Snake()
        self.obstacles = []
        self.food = self.generate_food()
        self.score = 0
        self.generate_obstacles(5)

    def generate_food(self):
        while True:
            x = random.randrange(0, WINDOW_WIDTH, BLOCK_SIZE)
            y = random.randrange(0, WINDOW_HEIGHT, BLOCK_SIZE)
            food_pos = (x, y)
            if (food_pos not in self.snake.positions and
                    food_pos not in self.obstacles):
                return food_pos

    def generate_obstacles(self, count):
        for _ in range(count):
            while True:
                x = random.randrange(0, WINDOW_WIDTH, BLOCK_SIZE)
                y = random.randrange(0, WINDOW_HEIGHT, BLOCK_SIZE)
                obstacle_pos = (x, y)
                if (obstacle_pos not in self.snake.positions and
                        obstacle_pos != self.food and
                        obstacle_pos not in self.obstacles):
                    self.obstacles.append(obstacle_pos)
                    break

    def check_food_collision(self):
        if self.snake.positions[0] == self.food:
            self.snake.grow()
            self.food = self.generate_food()
            self.score += 1
            if self.score % self.settings.obstacle_frequency == 0:
                self.generate_obstacles(1)

    def check_obstacle_collision(self):
        return self.snake.positions[0] in self.obstacles

    def draw(self):
        screen.fill(BLACK)

        for pos in self.snake.positions:
            pygame.draw.rect(screen, GREEN, (*pos, BLOCK_SIZE, BLOCK_SIZE))

        pygame.draw.rect(screen, RED, (*self.food, BLOCK_SIZE, BLOCK_SIZE))

        for obstacle in self.obstacles:
            pygame.draw.rect(screen, GRAY, (*obstacle, BLOCK_SIZE, BLOCK_SIZE))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Счет: {self.score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()


def run_game(settings):
    game = Game(settings)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game.snake.direction != "DOWN":
                    game.snake.direction = "UP"
                elif event.key == pygame.K_DOWN and game.snake.direction != "UP":
                    game.snake.direction = "DOWN"
                elif event.key == pygame.K_LEFT and game.snake.direction != "RIGHT":
                    game.snake.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and game.snake.direction != "LEFT":
                    game.snake.direction = "RIGHT"
                elif event.key == pygame.K_ESCAPE:
                    return "menu"

        game.snake.move()

        if game.snake.check_collision() or game.check_obstacle_collision():
            print(f"Игра окончена! Ваш счет: {game.score}")
            return "menu"

        game.check_food_collision()
        game.draw()
        clock.tick(settings.speed)


def main():
    menu = Menu()
    current_screen = "menu"

    while True:
        if current_screen == "menu":
            menu.draw_main_menu(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if menu.play_button.is_clicked(event.pos):
                        current_screen = run_game(menu.settings)
                    elif menu.settings_button.is_clicked(event.pos):
                        current_screen = "settings"
                    elif menu.exit_button.is_clicked(event.pos):
                        pygame.quit()
                        sys.exit()

        elif current_screen == "settings":
            menu.draw_settings_menu(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if menu.speed_up.is_clicked(event.pos):
                        menu.settings.speed = min(30, menu.settings.speed + 1)
                    elif menu.speed_down.is_clicked(event.pos):
                        menu.settings.speed = max(5, menu.settings.speed - 1)
                    elif menu.back_button.is_clicked(event.pos):
                        current_screen = "menu"


if __name__ == "__main__":
    main()
