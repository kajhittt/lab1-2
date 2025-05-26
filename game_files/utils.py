import pygame
import random
from game_files.config import SCREEN_WIDTH, SCREEN_HEIGHT, BONUS_IMAGE

def load_image(image_path, new_size=None):
    """Завантажити зображення з файла і змінити його розмір (якщо задано new_size)."""
    image = pygame.image.load(image_path)
    if new_size:
        image = pygame.transform.scale(image, new_size)
    return image

def create_car(x, y, car_image):
    """Створити об'єкт машини"""
    car = pygame.Rect(x, y, car_image.get_width(), car_image.get_height())
    return car

def create_bonus():
    """Створити бонус"""
    x = random.randint(50, SCREEN_WIDTH - 50)
    y = -50  # Початкове положення за межами екрана
    bonus = pygame.Rect(x, y, load_image(BONUS_IMAGE).get_width(), load_image(BONUS_IMAGE).get_height())
    return bonus