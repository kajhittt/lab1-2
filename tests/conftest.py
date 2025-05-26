# tests/conftest.py
import sys
import os
print(sys.path)
# Додаємо шлях до папки game_files в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../game_files')))
