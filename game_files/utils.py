import pygame
import random
from game_files.config import SCREEN_WIDTH, SCREEN_HEIGHT, BONUS_IMAGE

def load_image(image_path, new_size=None):
    """Завантажити зображення з файла і змінити його розмір (якщо задано new_size)."""
    image = pygame.image.load(image_path)
    if new_size:
        image = pygame.transform.scale(image, new_size)
    return image