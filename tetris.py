import pygame
import random
import os


pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 400, 800
BLOCK_SIZE = 40
COLUMNS = SCREEN_WIDTH // BLOCK_SIZE
ROWS = SCREEN_HEIGHT // BLOCK_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (200, 0, 0)
COLORS = [
    (255, 0, 0),  # Червоний
    (0, 255, 0),  # Зелений
    (0, 0, 255),  # Синій
    (255, 255, 0),  # Жовтий
    (0, 255, 255),  # Блакитний
    (255, 0, 255),  # Фіолетовий
    (255, 165, 0),  # Помаранчевий
    (128, 0, 128),  # Темно-фіолетовий
    (0, 128, 128),  # Морський синій
]

SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 1, 1],
     [1, 1, 0]],

    [[1, 1, 0],
     [0, 1, 1]],

    [[1, 1, 1, 1]],

    [[1, 1],
     [1, 1]],

    [[1, 1, 1],
     [1, 0, 0]],

    [[1, 1, 1],
     [0, 0, 1]],
]

# Екран
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

HIGH_SCORE_FILE = "high_score.txt"

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read())
    return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))

def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]

class Tetris:
    def __init__(self):
        self.board = [[0] * COLUMNS for _ in range(ROWS)]
        self.current_shape = random.choice(SHAPES)
        self.shape_color = random.choice(COLORS)
        self.shape_x = COLUMNS // 2 - len(self.current_shape[0]) // 2
        self.shape_y = 0
        self.game_over = False
        self.score = 0
        self.high_score = load_high_score()

    def can_move(self, dx, dy, shape=None):
        if shape is None:
            shape = self.current_shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.shape_x + x + dx
                    new_y = self.shape_y + y + dy
                    if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS or (new_y >= 0 and self.board[new_y][new_x]):
                        return False
        return True

    def freeze(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.shape_y + y][self.shape_x + x] = self.shape_color
        self.clear_lines()
        self.new_shape()

    def clear_lines(self):
        cleared_lines = 0
        self.board = [row for row in self.board if any(cell == 0 for cell in row)]
        cleared_lines = ROWS - len(self.board)
        while len(self.board) < ROWS:
            self.board.insert(0, [0] * COLUMNS)
        self.score += cleared_lines * 10
        if self.score > self.high_score:
            self.high_score = self.score
            save_high_score(self.high_score)

    def new_shape(self):
        self.current_shape = random.choice(SHAPES)
        self.shape_color = random.choice(COLORS)
        self.shape_x = COLUMNS // 2 - len(self.current_shape[0]) // 2
        self.shape_y = 0
        if not self.can_move(0, 0):
            self.game_over = True

    def move(self, dx, dy):
        if self.can_move(dx, dy):
            self.shape_x += dx
            self.shape_y += dy
        elif dy > 0:
            self.freeze()

    def rotate_shape(self):
        new_shape = rotate(self.current_shape)
        if self.can_move(0, 0, new_shape):
            self.current_shape = new_shape

    def draw_grid(self):
        for x in range(COLUMNS):
            for y in range(ROWS):
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, GRAY, rect, 1)

    def draw_text(self):
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        high_score_text = font.render(f"High Score: {self.high_score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 40))

    def draw_game_over(self):
        game_over_text = big_font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

    def draw(self):
        screen.fill(BLACK)
        self.draw_grid()
        self.draw_text()
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
        if not self.game_over:
            for y, row in enumerate(self.current_shape):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(screen, self.shape_color, ((self.shape_x + x) * BLOCK_SIZE, (self.shape_y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                        pygame.draw.rect(screen, WHITE, ((self.shape_x + x) * BLOCK_SIZE, (self.shape_y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
        else:
            self.draw_game_over()

clock = pygame.time.Clock()
tetris = Tetris()
fall_time = 0
speed = 500

def game_over_effect():
    for _ in range(5):
        screen.fill(RED)
        pygame.display.flip()
        pygame.time.delay(200)
        screen.fill(BLACK)
        pygame.display.flip()
        pygame.time.delay(200)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not tetris.game_over:
                if event.key == pygame.K_LEFT:
                    tetris.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    tetris.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    tetris.move(0, 1)
                elif event.key == pygame.K_UP:
                    tetris.rotate_shape()

    fall_time += clock.get_rawtime()
    clock.tick()

    if not tetris.game_over:
        if fall_time > speed:
            fall_time = 0
            tetris.move(0, 1)

    tetris.draw()
    pygame.display.flip()

    if tetris.game_over:
        game_over_effect()
        running = False

pygame.quit()
