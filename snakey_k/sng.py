
import pygame
import sys
import random

# Инициализация на Pygame
pygame.init()

# Настройки на прозореца
cell_size = 20
cell_number = 30
screen_size = cell_size * cell_number
screen = pygame.display.set_mode((screen_size, screen_size + 30))  # Увеличаваме височината на прозореца с 30 пиксела за score
clock = pygame.time.Clock()

# Зареждане на изображения
background_image = pygame.image.load("background.png")
head_image_1 = pygame.image.load("head.png")
head_image_2 = pygame.image.load("head2.png")
fruit_image = pygame.image.load("fruit.png")

# Оразмеряване на изображенията (1.5 пъти по-големи от клетките)
head_size = int(cell_size * 3)
fruit_size = int(cell_size * 2)

background_image = pygame.transform.scale(background_image, (screen_size, screen_size))
head_image_1 = pygame.transform.scale(head_image_1, (head_size, head_size))
head_image_2 = pygame.transform.scale(head_image_2, (head_size, head_size))
fruit_image = pygame.transform.scale(fruit_image, (fruit_size, fruit_size))

# Цветове за тялото на змията
SNAKE_COLOR_1 = (110, 163, 57)
SNAKE_COLOR_2 = (163, 69, 51)

# Зареждане на звуков файл за ядене на плодчето
eat_sound = pygame.mixer.Sound("eat_sound.wav")

# Зареждане на музика
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)  # Възпроизвеждане на музиката в продължение

# Клас за змията
class Snake:
    def __init__(self, color, keys, head_image):
        self.body = [[5, 10], [4, 10], [3, 10]]
        self.direction = [1, 0]
        self.new_block = False
        self.score = 0  # Инициализираме score на 0
        self.color = color
        self.keys = keys
        self.head_image = head_image

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, [self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1]])
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, [self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1]])
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True
        self.score += 1  # Увеличаваме score с 1 при изяден плод
        eat_sound.play()  # Възпроизвеждаме звука за ядене на плодчето

    def draw_snake(self):
        for block in self.body[1:]:
            pygame.draw.rect(screen, self.color, pygame.Rect(block[0] * cell_size, block[1] * cell_size, cell_size, cell_size))
        head = self.body[0]
        head_x = head[0] * cell_size - (head_size - cell_size) // 2
        head_y = head[1] * cell_size - (head_size - cell_size) // 2
        rotated_head = pygame.transform.rotate(self.head_image, self.get_head_angle())
        screen.blit(rotated_head, (head_x, head_y))
        
        # Рисуване на полукръг на последния блок на змията
        if len(self.body) > 1:
            last_block = self.body[-1]
            pygame.draw.circle(screen, self.color, (last_block[0] * cell_size + cell_size // 2, last_block[1] * cell_size + cell_size // 2), cell_size // 2)

    def get_head_angle(self):
        if self.direction == [1, 0]:  # Дясно
            return 90
        elif self.direction == [-1, 0]:  # Ляво
            return 270
        elif self.direction == [0, -1]:  # Нагоре
            return 180
        elif self.direction == [0, 1]:  # Надолу
            return 0

    def check_collision(self):
        # Проверка за колизия със стените
        if not 0 <= self.body[0][0] < cell_number or not 0 <= self.body[0][1] < cell_number:
            return True
        # Проверка за колизия със самата змия
        if self.body[0] in self.body[1:]:
            return True
        return False

# Клас за плода
class Fruit:
    def __init__(self):
        self.randomize()

    def randomize(self):
        self.position = [random.randint(0, cell_number - 1), random.randint(0, cell_number - 1)]

    def draw_fruit(self):
        fruit_x = self.position[0] * cell_size - (fruit_size - cell_size) // 2
        fruit_y = self.position[1] * cell_size - (fruit_size - cell_size) // 2
        screen.blit(fruit_image, (fruit_x, fruit_y))

# Основна игра
def main():
    while True:
        choice = game_mode_prompt()
        if choice == "single":
            singleplayer()
        elif choice == "multi":
            multiplayer()

def game_mode_prompt():
    screen.blit(background_image, (0, 0))
    font = pygame.font.Font(None, 74)
    text1 = font.render('1. Singleplayer', True, (255, 255, 255))
    text2 = font.render('2. Multiplayer', True, (255, 255, 255))
    rect1 = text1.get_rect(center=(screen_size / 2, screen_size / 2 - 40))
    rect2 = text2.get_rect(center=(screen_size / 2, screen_size / 2 + 40))
    screen.blit(text1, rect1)
    screen.blit(text2, rect2)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "single"
                elif event.key == pygame.K_2:
                    return "multi"

def singleplayer():
    snake = Snake(SNAKE_COLOR_1, {"UP": pygame.K_UP, "DOWN": pygame.K_DOWN, "LEFT": pygame.K_LEFT, "RIGHT": pygame.K_RIGHT}, head_image_1)
    fruit = Fruit()
    
    # Нулиране на score преди стартиране на нова игра
    snake.score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == snake.keys["UP"] and snake.direction != [0, 1]:
                    snake.direction = [0, -1]
                elif event.key == snake.keys["DOWN"] and snake.direction != [0, -1]:
                    snake.direction = [0, 1]
                elif event.key == snake.keys["LEFT"] and snake.direction != [1, 0]:
                    snake.direction = [-1, 0]
                elif event.key == snake.keys["RIGHT"] and snake.direction != [-1, 0]:
                    snake.direction = [1, 0]

        snake.move_snake()

        if snake.check_collision():
            game_over_prompt(snake.score, None)
            break

        if snake.body[0] == fruit.position:
            fruit.randomize()
            snake.add_block()

        screen.blit(background_image, (0, 0))
        snake.draw_snake()
        fruit.draw_fruit()
        draw_score(snake.score, None)
        pygame.display.update()
        clock.tick(7)

def multiplayer():
    snake1 = Snake(SNAKE_COLOR_1, {"UP": pygame.K_w, "DOWN": pygame.K_s, "LEFT": pygame.K_a, "RIGHT": pygame.K_d}, head_image_1)
    snake2 = Snake(SNAKE_COLOR_2, {"UP": pygame.K_UP, "DOWN": pygame.K_DOWN, "LEFT": pygame.K_LEFT, "RIGHT": pygame.K_RIGHT}, head_image_2)
    fruit = Fruit()
    
    # Нулиране на score преди стартиране на нова игра
    snake1.score = 0
    snake2.score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == snake1.keys["UP"] and snake1.direction != [0, 1]:
                    snake1.direction = [0, -1]
                elif event.key == snake1.keys["DOWN"] and snake1.direction != [0, -1]:
                    snake1.direction = [0, 1]
                elif event.key == snake1.keys["LEFT"] and snake1.direction != [1, 0]:
                    snake1.direction = [-1, 0]
                elif event.key == snake1.keys["RIGHT"] and snake1.direction != [-1, 0]:
                    snake1.direction = [1, 0]
                elif event.key == snake2.keys["UP"] and snake2.direction != [0, 1]:
                    snake2.direction = [0, -1]
                elif event.key == snake2.keys["DOWN"] and snake2.direction != [0, -1]:
                    snake2.direction = [0, 1]
                elif event.key == snake2.keys["LEFT"] and snake2.direction != [1, 0]:
                    snake2.direction = [-1, 0]
                elif event.key == snake2.keys["RIGHT"] and snake2.direction != [-1, 0]:
                    snake2.direction = [1, 0]

        snake1.move_snake()
        snake2.move_snake()

        if snake1.check_collision() and snake2.check_collision():
            game_over_prompt(snake1.score, snake2.score)
            break
        elif snake1.check_collision():
            game_over_prompt(0, snake2.score)
            break
        elif snake2.check_collision():
            game_over_prompt(snake1.score, 0)
            break

        if snake1.body[0] == fruit.position:
            fruit.randomize()
            snake1.add_block()

        if snake2.body[0] == fruit.position:
            fruit.randomize()
            snake2.add_block()

        screen.blit(background_image, (0, 0))
        snake1.draw_snake()
        snake2.draw_snake()
        fruit.draw_fruit()
        draw_score(snake1.score, snake2.score)
        pygame.display.update()
        clock.tick(7)

def draw_score(score1, score2):
    font = pygame.font.Font(None, 24)
    text1 = font.render(f'Player 1: {score1}', True, SNAKE_COLOR_1)
    text_rect1 = text1.get_rect(topleft=(10, screen_size + 5))
    screen.fill((0, 0, 0), text_rect1)  # Изтриваме само областта на стария score за Player 1
    screen.blit(text1, text_rect1)

    text_rect2 = None  # Инициализираме text_rect2 с None, преди да го използваме

    if score2 is not None:
        text2 = font.render(f'Player 2: {score2}', True, SNAKE_COLOR_2)
        text_rect2 = text2.get_rect(topright=(screen_size - 10, screen_size + 5))
        screen.fill((0, 0, 0), text_rect2)  # Изтриваме само областта на стария score за Player 2
        screen.blit(text2, text_rect2)

    pygame.display.update([text_rect1, text_rect2])  # Обновяваме само областите, където е променен текстът на score




def game_over_prompt(score1, score2):
    screen.blit(background_image, (0, 0))
    font = pygame.font.Font(None, 74)
    if score2 is None:
        text = font.render(f'Game Over! Score: {score1}', True, (255, 255, 255))
    else:
        if score1 > score2:
            winner = "Player 1 Wins!"
        elif score2 > score1:
            winner = "Player 2 Wins!"
        else:
            winner = "GAME OVER"
        text = font.render(winner, True, (255, 255, 255))
    rect = text.get_rect(center=(screen_size / 2, screen_size / 2))
    screen.blit(text, rect)
    pygame.display.flip()
    pygame.time.wait(2000)  # Изчакваме 2 секунди преди да покажем опции за рестарт/изход

    font_small = pygame.font.Font(None, 36)
    text_restart = font_small.render('Press R to Restart or Q to Quit', True, (255, 255, 255))
    rect_restart = text_restart.get_rect(center=(screen_size / 2, screen_size / 2 + 50))
    screen.blit(text_restart, rect_restart)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()
