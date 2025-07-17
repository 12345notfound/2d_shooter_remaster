import pygame

from variables import *
from typing import Literal


class SegmentLine:
    """Класс для удобных математических вычислений"""

    def __init__(self, pixel1, pixel2):
        self.coord_begin = pixel1
        self.coord_end = pixel2
        a, b, c = [pixel2[0] - pixel1[0], pixel1[1] - pixel2[1],
                   pixel1[1] * pixel2[1] - pixel1[1] * pixel1[1] - pixel1[0] * pixel2[0] + pixel1[0] * pixel1[0]]
        self.function = [a, b, c]
        self.function = list(map(lambda x: x / (a ** 2 + b ** 2 + c ** 2) ** 0.5, [a, b, c]))


def intersection_line(line1: SegmentLine, line2: SegmentLine):
    """Пересечение двух прямых"""
    a1, b1, c1 = line1.function
    a2, b2, c2 = line2.function
    z = (a1 * b2 - a2 * b1)
    if z == 0:
        z += 10 ** (-6)
    return [(b1 * c2 - b2 * c1) / z, (a2 * c1 - a1 * c2) / z]


class Obstacle(pygame.sprite.Sprite):
    """Класс препятсвия"""

    State = Literal["ACTIVE", "ABSENT"]

    def __init__(self, x, y, w, h, state):
        super().__init__(all_group.walls)
        self.rect = pygame.Rect(x, y, w, h)
        # self.image = pygame.surface.Surface((w, h))
        # self.image.fill((128, 128, 128))
        # self.mask = pygame.mask.from_surface(self.image)

        # состояния
        # STATE == "ACTIVE" активно
        # STATE == "ABSENT" отсутвует
        self.state = state


class Wall(Obstacle):
    """Класс стены (человек- ; свет-)"""

    def __init__(self, x, y, w, h, state: Literal["ACTIVE", "ABSENT"] = "ACTIVE"):
        super().__init__(x, y, w, h, state)
        vertex = [self.rect.topleft, self.rect.topright, self.rect.bottomright,
                  self.rect.bottomleft, self.rect.topleft]
        self.restrictive_line = [SegmentLine(vertex[i], vertex[i + 1]) for i in range(len(vertex) - 1)]


class Nightstand(Obstacle):
    """Класс тумбочки (человек- ; свет+)"""

    def __init__(self, x, y, w, h, state: Literal["ACTIVE", "ABSENT"] = "ACTIVE"):
        super().__init__(x, y, w, h, state)
        vertex = [self.rect.topleft, self.rect.topright, self.rect.bottomright,
                  self.rect.bottomleft, self.rect.topleft]
        self.restrictive_line = [SegmentLine(vertex[i], vertex[i + 1]) for i in range(len(vertex) - 1)]


class MapTexture(pygame.sprite.Sprite):
    """Текстуры карты"""

    def __init__(self, x, y):
        super().__init__(all_group.map_texture)
        self.image = all_sprites.map_image
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy
        if hasattr(obj, "set_hitbox"):
            obj.set_hitbox()

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Sprites():
    """Все текстуры и спрайты"""

    def __init__(self):
        self.im1 = pygame.image.load('1.png').convert()
        self.im1.set_colorkey((0, 0, 0))
        self.map_image = pygame.image.load('assets/map_100_texture.png')


class Groups():
    """Все группы"""

    def __init__(self):
        self.characters = pygame.sprite.Group()  # персонажи
        self.map_texture = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()


pygame.init()
screen = pygame.display.set_mode(size, pygame.DOUBLEBUF, 32)
pygame.mouse.set_visible(True)
all_sprites = Sprites()
all_group = Groups()
map_textur = MapTexture(0, 0)
camera = Camera()
