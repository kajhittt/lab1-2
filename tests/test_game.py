import pytest
from game_files.game import CarRacingGame
from unittest.mock import patch
import random

@pytest.fixture
def game():
    """Фікстура для створення об'єкта гри"""
    return CarRacingGame((255, 255, 255), "easy")

def test_spawn_obstacle(game):
    """Тестування створення машини-суперника"""
    initial_obstacles = len(game.obstacles)
    game.spawn_obstacle()
    assert len(game.obstacles) == initial_obstacles + 1

def test_spawn_bonus(game):
    """Тестування створення бонуса"""
    initial_bonuses = len(game.bonuses)
    game.spawn_bonus()
    assert len(game.bonuses) == initial_bonuses + 1

def test_check_collision_with_obstacle(game):
    """Тестування перевірки на зіткнення з машиною-перешкодою"""
    game.car = game.create_car(100, 100, game.car_image)  # задаємо місце для машини
    game.obstacles.append(game.create_car(100, 100, game.car_image))  # додамо машину на ту ж позицію
    game.check_collision()
    assert game.game_over == True

def test_check_collision_with_bonus(game):
    """Тестування перевірки на зіткнення з бонусом"""
    game.car = game.create_car(100, 100, game.car_image)
    
    # Створення бонуса в позиції, яка дозволяє зіткнутися з машиною
    bonus = game.create_bonus()
    bonus.x = 100  # Розміщуємо бонус на одній лінії з машиною
    bonus.y = 100
    game.bonuses.append(bonus)
    
    game.check_collision()
    
    # Перевірка, чи правильно оновлені очки
    assert game.score == 10  # За бонус має бути додано 10 очок
