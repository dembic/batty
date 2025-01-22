# objects.py

import pygame
import random
from settings import *
from utils import draw_text

class Bat:
    """Класс платформы."""
    def __init__(self):
        self.width = BAT_WIDTH
        self.height = BAT_HEIGHT
        self.speed = BAT_SPEED
        self.pos = [WIDTH // 2 - self.width // 2, HEIGHT - 50]
        self.jump = 0  # Анимация подпрыгивания
        self.color_index = 0  # Индекс текущего цвета
        self.colors = [
            (255, 0, 0),    # Красный
            (255, 165, 0),  # Оранжевый
            (255, 255, 0),  # Желтый
            (0, 255, 0),    # Зеленый
            (0, 0, 255),    # Синий
            (75, 0, 130),   # Индиго
            (238, 130, 238) # Фиолетовый
        ]
        self.color_timer = 0  # Таймер для смены цвета
        self.is_extended = False  # Флаг, указывающий, расширена ли платформа

    def move_left(self):
        """Движение платформы влево."""
        if self.pos[0] > 0:
            self.pos[0] -= self.speed

    def move_right(self):
        """Движение платформы вправо."""
        if self.pos[0] < WIDTH - self.width:
            self.pos[0] += self.speed

    def update_color(self):
        """Обновление цвета платформы."""
        if self.is_extended:  # Обновляем цвет только если платформа расширена
            if pygame.time.get_ticks() - self.color_timer > 100:  # Смена цвета каждые 100 мс
                self.color_index = (self.color_index + 1) % len(self.colors)
                self.color_timer = pygame.time.get_ticks()

    def draw(self, screen):
        """Отрисовка платформы."""
        self.update_color()  # Обновляем цвет
        color = self.colors[self.color_index] if self.is_extended else WHITE
        # Используем белый цвет, если платформа не расширена
        pygame.draw.rect(screen, self.colors[self.color_index],
                         (self.pos[0], self.pos[1] - self.jump, self.width, self.height))


class Ball:
    """Класс мяча."""
    def __init__(self):
        self.radius = BALL_RADIUS
        self.speed = BALL_SPEED.copy()
        self.pos = [WIDTH // 2, HEIGHT // 2]

    def update(self):
        """Обновление позиции мяча."""
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]

    def draw(self, screen):
        """Отрисовка мяча."""
        pygame.draw.circle(screen, RED, (int(self.pos[0]), int(self.pos[1])), self.radius)


class Tile:
    """Класс плитки."""
    def __init__(self, x, y, color, hits=1):
        self.rect = pygame.Rect(x, y, TILE_WIDTH, TILE_HEIGHT)
        self.color = color
        self.hits = hits  # Количество ударов для разрушения
        self.active = True

    def draw(self, screen):
        """Отрисовка плитки."""
        if self.active:
            pygame.draw.rect(screen, self.color, self.rect)
            if self.hits > 1:
                draw_text(screen, str(self.hits), self.rect.centerx, self.rect.centery - 5, font_size=20)


class Bonus:
    """Класс бонуса."""
    def __init__(self):
        self.radius = BONUS_RADIUS
        self.pos = [random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 200)]
        self.active = False
        self.animation_counter = 0

    def draw(self, screen):
        """Отрисовка бонуса."""
        if self.active:
            self.animation_counter += 1
            if self.animation_counter >= BONUS_ANIMATION_FRAMES:
                self.animation_counter = 0
            color = GREEN if self.animation_counter < BONUS_ANIMATION_FRAMES // 2 else BLUE
            pygame.draw.circle(screen, color, (int(self.pos[0]), int(self.pos[1])), self.radius)

class BonusText:
    """Класс для отображения текста бонуса и его анимации."""
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.timer = pygame.time.get_ticks() + 2000  # Таймер на 2 секунды
        self.particles = []  # Частицы для анимации рассыпания
        self.is_exploded = False  # Флаг, указывающий, началась ли анимация рассыпания

    def explode(self):
        """Создает частицы для анимации рассыпания текста."""
        for i in range(len(self.text) * 10):  # Создаем частицы для каждой буквы
            self.particles.append({
                "pos": [self.x + random.randint(-50, 50), self.y + random.randint(-50, 50)],
                "speed": [random.uniform(-2, 2), random.uniform(-2, 2)],
                "color": (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                "life": 60  # Время жизни частицы
            })
        self.is_exploded = True

    def update(self):
        """Обновление состояния текста и частиц."""
        if not self.is_exploded and pygame.time.get_ticks() >= self.timer:
            self.explode()  # Запускаем анимацию рассыпания

        for particle in self.particles:
            particle["pos"][0] += particle["speed"][0]
            particle["pos"][1] += particle["speed"][1]
            particle["life"] -= 1

    def draw(self, screen):
        """Отрисовка текста и частиц."""
        if not self.is_exploded:
            # Отрисовка текста
            draw_text(screen, self.text, self.x, self.y, font_size=30)
        else:
            # Отрисовка частиц
            for particle in self.particles:
                if particle["life"] > 0:
                    pygame.draw.circle(screen, particle["color"],
                                       (int(particle["pos"][0]), int(particle["pos"][1])), 3)

class TileExplosion:
    """Класс анимации разрушения плитки."""
    def __init__(self, x, y):
        self.particles = []
        for _ in range(20):  # 20 частиц
            self.particles.append({
                "pos": [x, y],
                "speed": [random.uniform(-2, 2), random.uniform(-2, 2)],
                "color": (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                "life": 30
            })

    def update(self):
        """Обновление частиц."""
        for particle in self.particles:
            particle["pos"][0] += particle["speed"][0]
            particle["pos"][1] += particle["speed"][1]
            particle["life"] -= 1

    def draw(self, screen):
        """Отрисовка частиц."""
        for particle in self.particles:
            if particle["life"] > 0:
                pygame.draw.circle(screen, particle["color"], (int(particle["pos"][0]), int(particle["pos"][1])), 3)


class BonusEffect:
    """Класс эффекта бонуса."""
    def __init__(self, x, y):
        self.particles = []
        for _ in range(20):  # 20 частиц
            self.particles.append({
                "pos": [x, y],
                "speed": [random.uniform(-2, 2), random.uniform(-2, 2)],
                "color": (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                "life": 30
            })

    def update(self):
        """Обновление частиц."""
        for particle in self.particles:
            particle["pos"][0] += particle["speed"][0]
            particle["pos"][1] += particle["speed"][1]
            particle["life"] -= 1

    def draw(self, screen):
        """Отрисовка частиц."""
        for particle in self.particles:
            if particle["life"] > 0:
                pygame.draw.circle(screen, particle["color"], (int(particle["pos"][0]), int(particle["pos"][1])), 3)