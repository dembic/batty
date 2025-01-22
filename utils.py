# utils.py

import pygame
from settings import *

def draw_text(screen, text, x, y, color=WHITE, font_size=FONT_SIZE):
    """Отрисовка текста на экране."""
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def load_sounds():
    """Загрузка звуковых эффектов и музыки."""
    pygame.mixer.init()
    sounds = {
        "hit": pygame.mixer.Sound(SOUND_HIT),
        "lose": pygame.mixer.Sound(SOUND_LOSE),
        "bonus": pygame.mixer.Sound(SOUND_BONUS),
    }
    pygame.mixer.music.load(MUSIC_BACKGROUND)
    return sounds

def play_music():
    """Запуск фоновой музыки."""
    pygame.mixer.music.play(-1)