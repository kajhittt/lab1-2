import argparse
from game_files.config import BACKGROUND_COLOR

def parse_arguments():
    parser = argparse.ArgumentParser(description="Настройки гри Car Racing")
    parser.add_argument('--difficulty', type=str, default='easy', choices=['easy', 'medium', 'hard'],
                        help='Вибір складності гри')
    parser.add_argument('--bg_color', type=str, default='255,255,255', help='Колір фону у форматі RGB')
    return parser.parse_args()

def get_background_color(args):
    # Парсимо колір фону у формат RGB
    color = tuple(map(int, args.bg_color.split(',')))
    return color