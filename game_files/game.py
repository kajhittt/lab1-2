import pygame
import random  # Імпортуємо стандартний модуль random
from game_files.config import SCREEN_WIDTH, SCREEN_HEIGHT, ROAD_IMAGE, CAR_IMAGE, BONUS_IMAGE, EXPLOSION_IMAGE, FPS
from game_files.settings import get_background_color
from game_files.utils import load_image, create_car, create_bonus

class CarRacingGame:
    def __init__(self, background_color, difficulty):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Car Racing Game')
        self.clock = pygame.time.Clock()

        # Завантажуємо зображення
        self.background = load_image(ROAD_IMAGE, new_size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.car_image = load_image(CAR_IMAGE, new_size=(50, 100))  # Розмір машини 50x100
        self.bonus_image = load_image(BONUS_IMAGE, new_size=(30, 30))  # Розмір бонуса 30x30
        self.explosion_image = load_image(EXPLOSION_IMAGE, new_size=(100, 100))  # Розмір вибуху 100x100

        # Колір фону та складність
        self.background_color = background_color
        self.difficulty = difficulty
        self.speed = self.set_speed()

        # Ініціалізація машини та інших параметрів
        self.car = self.create_car(SCREEN_WIDTH // 2 - self.car_image.get_width() // 2, SCREEN_HEIGHT - 120, self.car_image)
        self.bonuses = []
        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.explosion_pos = None  # Позиція вибуху
        self.explosion_timer = 0  # Таймер для вибуху

    def set_speed(self):
        """Визначаємо швидкість в залежності від складності"""
        if self.difficulty == 'easy':
            return 3
        elif self.difficulty == 'medium':
            return 5
        else:
            return 7

    def spawn_obstacle(self):
        """Створюємо нову машину-суперника та перевіряємо на колізії"""
        while True:
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = -50
            obstacle = pygame.Rect(x, y, self.car_image.get_width(), self.car_image.get_height())
            # Перевірка на колізії з іншими перешкодами
            if not any(obstacle.colliderect(other) for other in self.obstacles):
                self.obstacles.append(obstacle)
                break

    def spawn_bonus(self):
        """Створюємо бонус"""
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = -30
        bonus = pygame.Rect(x, y, self.bonus_image.get_width(), self.bonus_image.get_height())
        self.bonuses.append(bonus)

    def create_car(self, x, y, image):
        """Метод для створення машини"""
        car_rect = pygame.Rect(x, y, image.get_width(), image.get_height())
        return car_rect

    def create_bonus(self):
        """Метод для створення бонуса"""
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = -30
        bonus = pygame.Rect(x, y, self.bonus_image.get_width(), self.bonus_image.get_height())
        return bonus

    def check_collision(self):
        """Перевірка на зіткнення з машинами та бонусами"""
        for obstacle in self.obstacles:
            if self.car.colliderect(obstacle):
                self.game_over = True
                self.explosion_pos = self.car.center  # Встановлюємо позицію вибуху в центр машини
        
        for bonus in self.bonuses:
            if self.car.colliderect(bonus):
                self.bonuses.remove(bonus)  # Видаляємо бонус після зіткнення
                self.score += 10  # Додаємо 10 очок за бонус

    def run(self):
        """Основний цикл гри"""
        running = True
        while running:
            self.screen.fill(self.background_color)  # Заповнюємо фон кольором
            self.screen.blit(self.background, (0, 0))  # Малюємо дорогу

            # Обробка подій
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and self.game_over:
                    if event.key == pygame.K_r:  # Перезапуск гри
                        self.__init__(self.background_color, self.difficulty)  # Перезапускаємо гру
                    if event.key == pygame.K_q:  # Вихід з гри
                        running = False

            # Оновлення позиції машини
            if not self.game_over:  # Якщо гра не завершена
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and self.car.left > 0:
                    self.car.move_ip(-5, 0)
                if keys[pygame.K_RIGHT] and self.car.right < SCREEN_WIDTH:
                    self.car.move_ip(5, 0)

                # Спавнимо машини-суперників і бонуси
                if random.randint(0, 100) < self.speed:
                    self.spawn_obstacle()

                if random.randint(0, 300) == 0:  # Час від часу створюємо бонус
                    self.spawn_bonus()

                # Оновлення позиції машин
                for obstacle in self.obstacles[:]:
                    obstacle.move_ip(0, self.speed)
                    if obstacle.top > SCREEN_HEIGHT:
                        self.obstacles.remove(obstacle)

                for bonus in self.bonuses[:]:
                    bonus.move_ip(0, 3)
                    if bonus.top > SCREEN_HEIGHT:
                        self.bonuses.remove(bonus)

                # Перевірка на зіткнення
                self.check_collision()

            # Малюємо машини-суперники
            for obstacle in self.obstacles:
                self.screen.blit(self.car_image, obstacle)

            # Малюємо бонуси
            for bonus in self.bonuses:
                self.screen.blit(self.bonus_image, bonus)

            # Малюємо машину гравця
            self.screen.blit(self.car_image, self.car)

            # Малюємо вибух (якщо він є)
            if self.explosion_pos:
                self.screen.blit(self.explosion_image, (self.explosion_pos[0] - self.explosion_image.get_width() // 2,
                                                        self.explosion_pos[1] - self.explosion_image.get_height() // 2))

            # Виведення очок
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Очки: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))

            # Якщо гра завершена
            if self.game_over:
                game_over_text1 = font.render("Гра закінчена!", True, (255, 0, 0))
                game_over_text2 = font.render("Натисніть R для перезапуску або Q для виходу", True, (255, 0, 0))
                self.screen.blit(game_over_text1, ((SCREEN_WIDTH - game_over_text1.get_width()) // 2, (SCREEN_HEIGHT // 2) - 30))
                self.screen.blit(game_over_text2, ((SCREEN_WIDTH - game_over_text2.get_width()) // 2, (SCREEN_HEIGHT // 2) + 30))

            # Оновлення екрану
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()