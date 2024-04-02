from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Середина игровой области
SCREEN_CENTER = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Толщина границы ячейки
BORDER_THICKNESS = 1

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Минимальная длина змеи, которая может себя укусить
MIN_SELF_COLLISION_SNAKE_LENGTH = 4


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self, body_color=None):
        self.position = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.body_color = body_color

    def draw(self):
        """Отрисовка объекта"""
        raise NotImplementedError(
            f'Определите draw в {self.__class__.__name__}'
        )

    def draw_cell(self, position, color=None):
        """Отрисовка квадратика"""
        color = color if color else self.body_color
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        if color != BOARD_BACKGROUND_COLOR:
            pygame.draw.rect(screen, BORDER_COLOR, rect, BORDER_THICKNESS)


class Snake(GameObject):
    """Класс описывающий змейку и её поведение"""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.reset()

    def draw(self):
        """Отрисовка змейки"""
        self.draw_cell(self.get_head_position())
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

    def move(self):
        """Движение змейки по игровому полю"""
        head_x, head_y = self.positions[0]
        direction_x, direction_y = self.direction

        position = (
            (head_x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH,
            (head_y + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT
        )
        self.positions.insert(0, position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self, new_direction):
        """обновляет направление движения змейки"""
        self.direction = new_direction

    def get_head_position(self):
        """возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """сбрасывает змейку в начальное состояние после столкновения"""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None


class Apple(GameObject):
    """Класс описывающий яблоко"""

    def __init__(self,
                 occupied_positions=(SCREEN_CENTER,),
                 body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.soccupied_positions = occupied_positions
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """устанавливает случайное положение яблока"""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in occupied_positions:
                break

    def draw(self):
        """отрисовывает яблоко"""
        self.draw_cell(self.position)


def handle_keys(game_object: Snake):
    """обрабатывает нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.K_ESCAPE:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit


def main():
    """основной цикл игры"""
    snake = Snake()
    apple = Apple(snake.positions)

    screen.fill(BOARD_BACKGROUND_COLOR)
    print('Starting game...')

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        if (snake.get_head_position() in
                snake.positions[MIN_SELF_COLLISION_SNAKE_LENGTH:]):
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)
        elif snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
