# Настройки окна
WIDTH = 800
HEIGHT = 600
FPS = 60  # Добавлено

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [RED, GREEN, BLUE, YELLOW]  # Цвета плиток

# Параметры платформы
BAT_WIDTH = 100
BAT_HEIGHT = 20
BAT_SPEED = 10

# Параметры мяча
BALL_RADIUS = 10
BALL_SPEED = [5, -5]  # Начальная скорость мяча

# Уровни сложности
LEVELS = [
    {
        "tiles": [
            {"color": RED, "hits": 1},
            {"color": GREEN, "hits": 2},
            {"color": BLUE, "hits": 3},
        ],
        "ball_speed": [5, -5]
    },
    {
        "tiles": [
            {"color": YELLOW, "hits": 1},
            {"color": BLUE, "hits": 2},
            {"color": RED, "hits": 3},
        ],
        "ball_speed": [6, -6]
    },
]

# Параметры плиток
TILE_WIDTH = (WIDTH - 9 * 5) // 8  # Ширина плитки с учетом отступов
TILE_HEIGHT = 20  # Высота плитки
TILE_PADDING = 5  # Расстояние между плитками
TILE_OFFSET_Y = 50  # Смещение плиток вниз от верхнего края

# Бонусы
BONUS_TYPES = ["extend_bat", "slow_ball", "extra_life", "speed_up", "multi_ball", "invisibility"]
BONUS_RADIUS = 15
BONUS_ANIMATION_FRAMES = 10

# Звуковые эффекты и музыка
SOUND_HIT = "hit.wav"
SOUND_LOSE = "lose.wav"
SOUND_BONUS = "bonus.wav"
MUSIC_BACKGROUND = "background_music.mp3"

# Шрифт
FONT_SIZE = 36