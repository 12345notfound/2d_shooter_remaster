from PIL import Image
from classes_and_functions_tier1 import *


def all_wall(filename):
    """считывает все стены"""
    # функция будет менять взависимости от типа карты

    im = Image.open(filename)
    pixels = im.load()
    x, y = im.size

    list_all_wall = []
    for i in range(x):
        for j in range(y):
            if pixels[i, j][:3] == (237, 28, 36):
                list_all_wall.append(Wall(i * 50, j * 50, 50, 50))
            elif pixels[i, j][:3] == (195, 195, 195):
                list_all_wall.append(Nightstand(i * 50, j * 50, 50, 50))
    return list_all_wall


def len_map(filename):
    """длинна карты игрока"""

    im = Image.open(filename)
    x, y = im.size
    return x * 50, y * 50


def smashes_walls_blocks(filename):
    """разбивает все стены на блоки"""

    list_all_wall = all_wall(filename)
    x, y = len_map(filename)
    result = [[[] for _ in range(y // len_split_wall + 1)] for _ in range(x // len_split_wall + 1)]

    for wall in list_all_wall:
        for i in range(wall.rect.topleft[0] // len_split_wall, wall.rect.topright[0] // len_split_wall + 1):
            for j in range(wall.rect.topleft[1] // len_split_wall, wall.rect.bottomleft[1] // len_split_wall + 1):
                result[i][j].append(wall)

    return result


wall_door = smashes_walls_blocks('assets/map100.png')
