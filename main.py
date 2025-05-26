import pygame
from game_files.settings import parse_arguments, get_background_color
from game_files.game import CarRacingGame

def main():
    # Отримуємо аргументи командного рядка
    args = parse_arguments()

    # Отримуємо колір фону з аргументів
    background_color = get_background_color(args)

    # Ініціалізуємо гру
    game = CarRacingGame(background_color, args.difficulty)
    game.run()

if __name__ == '__main__':
    pygame.init()
    main()