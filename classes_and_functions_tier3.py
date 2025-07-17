import pygame

from common_functions_tier2 import *
from wall_arrangement_tier2 import *


class Entity(pygame.sprite.Sprite):
    """Общий класс сущности"""

    def __init__(self, x, y, sprite_entity):
        super().__init__(all_group.characters)
        self.IMAGE = sprite_entity
        self.image = sprite_entity
        self.rect = self.image.get_rect()
        self.rect.center = (round(x), round(y))
        self.real_coordinate = (x, y)

        self.hitbox = self.image.get_rect(width=57, height=57)
        self.hitbox.center = self.rect.center
        self.hitbox.centerx += 4

    def set_hitbox(self):
        """выставляет хитбокс в нужное место"""

        self.hitbox = self.image.get_rect(width=54, height=54)
        self.hitbox.center = self.rect.center


class Player(Entity):
    """Класс игрока"""

    def __init__(self, x, y, sprite_entity):
        super().__init__(x, y, sprite_entity)

    def update(self):
        xshift = 0
        yshift = 0

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_w]:
            yshift -= speed_entity
        if keystate[pygame.K_s]:
            yshift += speed_entity
        if keystate[pygame.K_a]:
            xshift -= speed_entity
        if keystate[pygame.K_d]:
            xshift += speed_entity

        test_rect = self.hitbox
        test_rect.centerx, test_rect.centery = test_rect.centerx + xshift, test_rect.centery + yshift
        if not defining_intersection(test_rect):
            self.rect.centerx, self.rect.centery = self.rect.centerx + xshift, self.rect.centery + yshift

        # поворот персонажа к курсору
        self.direction = determining_angle(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        self.image = pygame.transform.rotate(self.IMAGE, self.direction + 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen):
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox)
        screen.blit(self.image, self.rect)


def defining_intersection_pixel_object(coordinates, obstacle):
    pass


def defining_intersection_pixel(coordinates):
    """проверяет принадлежность пикселя к препятсвию или двери"""

    x, y = coordinates
    x, y = translation_coordinates(x, y)
    rect_map_object = pygame.Rect((x, y, 1, 1))
    if rect_map_object.collidelist(
            list(map(lambda x: x.rect, wall_door[x // len_split_wall][y // len_split_wall]))) == -1:
        return False
    return True


def defining_intersection(rect_object: pygame.Rect):
    """проверяет пересечение прямоугольного объекта со стенами и дверями"""
    # Важно, чтобы длинна объекта была меньше разбиения на блоки

    pixels = [rect_object.topleft, (rect_object.topright[0] - 1, rect_object.topright[1]),
              (rect_object.bottomleft[0], rect_object.bottomleft[1] - 1),
              (rect_object.bottomright[0] - 1, rect_object.bottomright[1] - 1)]
    pixels = list(map(lambda coordinate: defining_intersection_pixel(coordinate), pixels))
    return any(pixels)
