import pygame

from classes_and_functions_tier3 import *


# from imageformat import *
# def pic_to_map(filename):
#     """Переводит картинку в карту"""
#
#     im = Image.open(filename)
#     pixels = im.load()
#     x, y = im.size
#     result = [[False for _ in range(y)] for _ in range(x)]
#
#     for i in range(x):
#         for j in range(y):
#             if pixels[i, j][:3] == (237, 28, 36):
#                 Wall(i * 50, j * 50)
#                 result[i][j] = True
#             elif pixels[i, j][:3] == (34, 177, 76):
#                 if pixels[i + 1, j][:3] == (255, 242, 0):
#                     Door(i * 50 + 25, j * 50, 1)
#                     result[i][j] = [True, 1]
#                     result[i + 1][j] = [True, 1]
#                 else:
#                     Door(i * 50, j * 50 + 25, 0)
#                     result[i][j + 1] = [True, 0]
#                     result[i][j] = [True, 0]
#             elif pixels[i, j][:3] == (195, 195, 195):
#                 result[i][j] = 3
#
#     # возвращает массив с расположнием стен и дверей
#     return result









def updating_coordinates(target):
    camera.update(target)
    for entity in all_group.characters:
        camera.apply(entity)
    for entity in all_group.map_texture:
        camera.apply(entity)


def draw_object():
    # characters.draw(screen)
    all_group.map_texture.draw(screen)
    for entity in all_group.characters:
        entity.draw(screen)


def update_object():
    """обновляем все объекты"""

    for entity in all_group.characters:
        entity.update()


if __name__ == '__main__':
    hero = Player(4550, 4280, all_sprites.im1)
    pygame.display.flip()



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        update_object()
        updating_coordinates(hero)
        draw_object()

        fps = clock.get_fps()  # Вызываем функцию для получения FPS
        print("FPS: ", fps)
        clock.tick(FPS)
        pygame.display.flip()
