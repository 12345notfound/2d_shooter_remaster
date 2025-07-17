from classes_and_functions_tier1 import *
from math import sin, radians, cos, asin, pi, degrees


def determining_angle(x, y, x_pos=width // 2, y_pos=height // 2):
    """считает угол между двумя пикселями"""

    # расчеты производятся относительно второго пикселя
    if y_pos != y or x_pos != x:
        turn = pi / 2 - asin(((y_pos - y) / (
                (x_pos - x) ** 2 + (y_pos - y) ** 2) ** 0.5))
        if x_pos > x:
            turn = degrees(turn)
        else:
            turn = -degrees(turn)
    else:
        return 0
    return turn


def translation_coordinates(x, y):
    """переводит координату пикселя на экране, в координату пикселя на карте"""

    return (x - map_textur.rect.x), (y - map_textur.rect.y)
