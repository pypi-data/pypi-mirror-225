import random


def get_random_icon() -> str:
    icons = [
        '🐶', '🐱', '🐭', '🐹', '🦊', '🐻', '🐨', '🐯', '🦁', '🐮', '🐷', '🍎', '🍐',
        '🍊', '🍋', '🍌', '🍉', '🍇', '🍓', '🍈', '🍒', '🍑'
    ]
    return random.choice(icons)
