import pygame
import sqlite3
import hashlib
import os
import random
from math import sin, radians, cos, asin, pi, degrees
from PIL import Image








def pic_to_map(filename):
    """Переводит картинку в карту"""

    im = Image.open(filename)
    pixels = im.load()
    x, y = im.size
    result = [[False for _ in range(y)] for _ in range(x)]

    for i in range(x):
        for j in range(y):
            if pixels[i, j][:3] == (237, 28, 36):
                Wall(i * 50, j * 50)
                result[i][j] = True
            elif pixels[i, j][:3] == (34, 177, 76):
                if pixels[i + 1, j][:3] == (255, 242, 0):
                    Door(i * 50 + 25, j * 50, 1)
                    result[i][j] = [True, 1]
                    result[i + 1][j] = [True, 1]
                else:
                    Door(i * 50, j * 50 + 25, 0)
                    result[i][j + 1] = [True, 0]
                    result[i][j] = [True, 0]
            elif pixels[i, j][:3] == (195, 195, 195):
                result[i][j] = 3

    # возвращает массив с расположнием стен и дверей
    return result


const = 0
constx = 25
consty = 25


def translation_coordinates(x, y):
    '''переводит аюсолютную координату относительно расположения пикселя на карте'''

    return (x + player.real_posx - player.rect.centerx + constx,
            y + player.real_posy - player.rect.centery + consty)


def data_translation(pixelx, pixely, who):
    """для правильного считывания информации из массива"""

    if type(wall_layout[pixelx // 50][pixely // 50]) == list:
        if wall_layout[pixelx // 50][pixely // 50][1] == 1:
            if abs(pixely / 50 - int(pixely / 50) - 0.5) <= 0.2:
                return wall_layout[pixelx // 50][pixely // 50][0]
            else:
                return False
        else:
            if abs(pixelx / 50 - int(pixelx / 50) - 0.5) <= 0.2:
                return wall_layout[pixelx // 50][pixely // 50][0]
            else:
                return False
    elif wall_layout[pixelx // 50][pixely // 50] == 3:
        if who == 'entity':
            return True
        else:
            return False
    return wall_layout[pixelx // 50][pixely // 50]


def defining_intersection(coord, size_x, size_y, who):
    '''проверяет на принадлежность к стене или двери'''

    x_real, y_real = int(coord[0]), int(coord[1])
    if size_x == 1 and size_y == 1:
        return data_translation(x_real, y_real, who)
    else:
        return data_translation(x_real, y_real, who) or data_translation((x_real + size_x - 1), (y_real + size_y - 1),
                                                                         who) or \
               data_translation((x_real + size_x - 1), y_real, who) or data_translation(x_real, (y_real + size_y - 1),
                                                                                        who) or \
               data_translation((x_real + size_x // 2), y_real, who) or data_translation(x_real, (y_real + size_y // 2),
                                                                                         who) or \
               data_translation((x_real + size_x // 2), (y_real + size_y - 1), who) or \
               data_translation((x_real + size_x - 1), (y_real + size_y // 2), who)


def draw_flashlight(points, color):
    """отрисовывает фонаря"""

    # отрисовка видимости игрока
    surface1 = pygame.Surface(size)
    surface1.set_alpha(150)
    pygame.draw.polygon(surface1, color, points)
    pygame.draw.polygon(surface1, (255, 255, 255), points, width=2)
    screen.blit(surface1, (0, 0))




class Entity(pygame.sprite.Sprite):
    """Общий класс сущности"""

    def __init__(self, x, y):
        super().__init__(all_sprites, characters)
        self.image = im1
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.real_posx = x
        self.real_posy = y

        self.health = 10
        self.max_health = 10
        self.damage = 5
        self.direction = 0



    def get_nearest_door(self):
        """Возвращает ближайшую к игроку дверь"""

        min_dist = 1000000000000  # очень большая константа
        nearest_door = None  # ближайшая дверь
        for door in doors:
            if (self.rect.centerx - door.rect.centerx) ** 2 + (
                    self.rect.centery - door.rect.centery) ** 2 < min_dist:
                min_dist = (
                                   self.rect.centerx - door.rect.centerx) ** 2 + (
                                   self.rect.centery - door.rect.centery) ** 2
                nearest_door = door
        return nearest_door






    def anim_is_idle_update(self):
        if self.rect.center != self.prev_pos:
            self.anim_idle_cnt = 0
            self.is_idle = False
            self.is_moving = True
        else:
            self.is_idle = True
            self.is_moving = False
            self.anim_idle_cnt = (self.anim_idle_cnt + 1) % 60

    def anim_is_moving_update(self):
        if self.rect.center == self.prev_pos:
            self.anim_move_cnt = 0
            self.is_moving = False
            self.is_idle = True
        else:
            self.is_moving = True
            self.is_idle = False
            self.anim_move_cnt = (self.anim_move_cnt + 1) % 60


    def move_entity(self, x, y):
        """Переместить сущность на координаты х, y"""
        self.prev_pos = self.rect.center  # для анимаций
        start_x, start_y = self.real_posx, self.real_posy
        self.real_posx = start_x + x
        self.real_posy = start_y + y
        x_move, y_move, xy_move = True, True, True
        if defining_intersection(
                (self.real_posx - 32 + constx, self.real_posy - 32 + consty),
                64, 64, 'entity'):
            xy_move = False
        self.real_posx = start_x + x
        self.real_posy = start_y
        if defining_intersection(
                (self.real_posx - 32 + constx, self.real_posy - 32 + consty),
                64, 64, 'entity'):
            x_move = False
        self.real_posx = start_x
        self.real_posy = start_y + y
        if defining_intersection(
                (self.real_posx - 32 + constx, self.real_posy - 32 + consty),
                64, 64, 'entity'):
            y_move = False
        if xy_move:
            self.movement = True
            self.rect.centerx += x
            self.rect.centery += y
            self.real_posx = start_x + x
            self.real_posy = start_y + y
        elif x_move:
            self.movement = True
            self.rect.centerx += x
            self.real_posx = start_x + x
            self.real_posy = start_y
        elif y_move:
            self.movement = True
            self.rect.centery += y
            self.real_posx = start_x
            self.real_posy = start_y + y
        else:
            self.movement = True
            self.real_posx = start_x
            self.real_posy = start_y
        if x == 0 and y == 0:
            self.movement = False
        if type(self) == Player:
            self.wall_hitbox.center = self.rect.center

    def draw_health_bar(self, health_color, health):
        pygame.draw.rect(screen, width=1, rect=(
            self.rect.centerx - 26, self.rect.centery - 50, 52, 12), color='black')
        pygame.draw.rect(screen, width=0,
                         rect=(self.rect.centerx - 25, self.rect.centery - 49,
                               int(50 * health / self.max_health), 10),
                         color=health_color)

    def determining_angle(self, x_pos, y_pos, x, y):
        """считает кгол между двумя пикселями"""

        # расчеты производятся относительно первого пикселя
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

    def beam(self, x_start, y_start, x_end=False, y_end=False, turn=0, long=500,
             nesting=1, accuracy=0):
        """рисует луч с учетом пересечений со стенами"""
        # вернет кортеж, где первый аргумент - смог ли луч добрать до конечной точки,
        # а второй - точку где он впервые пересек стену или дверь

        # выставляет значение точности
        if accuracy == 0:
            if nesting == 1:
                accuracy = 40
            else:
                accuracy = 15

        # подсчитывае скорость перемещения пикселя "проверки"
        if x_end and y_end:
            x_speed = (x_end - x_start) / accuracy
            y_speed = (y_end - y_start) / accuracy
        else:
            x_speed = -sin(radians(turn)) * long / accuracy
            y_speed = -cos(radians(turn)) * long / accuracy

        # находит первое пересение луча со стеной или дверью
        for i in range(0, accuracy + 1):
            x, y = int(x_start + x_speed * i), int(y_start + y_speed * i)
            if defining_intersection(translation_coordinates(x, y), 1, 1, 'beam'):
                if nesting == 1:
                    return (False, self.beam(x - x_speed, y - y_speed, x_end=x,
                                             y_end=y, nesting=2)[1])
                else:
                    return (False, (x, y))
        return (True, (x, y))


class Player(Entity):
    """Класс игрока"""

    def __init__(self, x, y):
        super().__init__(x, y)
        characters_rendering.add(self)
        self.current_weapon = 1
        self.medkits = 0
        self.range = 15000
        self.max_health = self.health = 100
        self.wall_hitbox = self.image.get_rect(center=self.rect.center, width=54, height=54)
        self.wall_hitbox.h = self.wall_hitbox.w = 54

    def kill(self):
        self.end_game()

    def end_game(self):
        """конец игры"""
        global running, end_False_run
        running = False
        end_False_run = True



    def draw_interface(self):
        """Отрисовка интерфейса игрока"""
        self.font = pygame.font.Font(None, 30)
        self.ammo_str = self.font.render(str(self.medkits), True,
                                         (255, 255, 255))
        screen.blit(self.ammo_str, (int(width * 0.88), int(height * 0.80)))
        screen.blit(medkit_image, (int(width * 0.868), int(height * 0.84)))

        pygame.draw.rect(screen, width=1, rect=(
            int(width * 0.1), int(height * 0.8), 100, 30),
                         color='black')
        pygame.draw.rect(screen, width=0,
                         rect=(int(width * 0.1) + 1, int(height * 0.8) + 1,
                               100 * self.health / self.max_health, 30),
                         color='green')
        self.health_str = self.font.render(f'{self.health}/{self.max_health}', True, (255, 255, 255))
        screen.blit(self.health_str, (int(width * 0.1) + 15, int(height * 0.8) + 40))

    def get_nearest_door(self):
        """Возвращает ближайшую к игроку дверь"""
        min_dist = 1000000000000  # очень большая константа
        nearest_door = None  # ближайшая дверь
        for door in doors:
            if (player.rect.centerx - door.rect.centerx) ** 2 + (
                    player.rect.centery - door.rect.centery) ** 2 < min_dist:
                min_dist = (
                                   player.rect.centerx - door.rect.centerx) ** 2 + (
                                   player.rect.centery - door.rect.centery) ** 2
                nearest_door = door
        return nearest_door

    def get_nearest_lootbox(self):
        """Возвращает ближайший к игроку ящик"""
        min_dist = 1000000000000  # очень большая константа
        nearest_lootbox = None  # ближайшая коробка
        for lootbox in lootboxes:
            if (player.rect.centerx - lootbox.rect.centerx) ** 2 + (
                    player.rect.centery - lootbox.rect.centery) ** 2 < min_dist:
                min_dist = (
                                   player.rect.centerx - lootbox.rect.centerx) ** 2 + (
                                   player.rect.centery - lootbox.rect.centery) ** 2
                nearest_lootbox = lootbox
        return nearest_lootbox

    def tracing(self):
        """происходит трассировка лучей для фонарика"""

        self.viewing_angle = 60  # угол обзора
        coord = [(width // 2,
                  height // 2)]  # массив координат многоугольника, для создания фонаря (видимости)
        turn = 1  # частота пускания лучей (угол между соседними лучами)

        # выполняется трассировка
        for i in range(int(self.viewing_angle / turn) + 1):
            coord.append(
                self.beam(width // 2, height // 2,
                          turn=self.direction - self.viewing_angle / 2 + i * turn,
                          long=500)[1])
        coord.append((width // 2, height // 2))

        draw_flashlight(coord, (255, 255, 173, 50))

    def visible_objects(self):
        for enemy in enemies:
            dist = (enemy.real_posx - self.real_posx) ** 2 + (
                    enemy.real_posy - self.real_posy) ** 2
            if dist <= 10000:
                enemy.distance_beam = [True, True]
                if not enemy in characters_rendering:
                    characters_rendering.add(enemy)
            elif dist <= 530 ** 2:
                if self.beam(self.rect.centerx, self.rect.centery,
                             x_end=enemy.rect.centerx, y_end=enemy.rect.centery,
                             accuracy=30, nesting=2)[0]:
                    enemy.distance_beam = [False, True]
                    if abs(self.direction - self.determining_angle(
                            self.rect.centerx, self.rect.centery,
                            enemy.rect.centerx,
                            enemy.rect.centery)) <= 34 or abs(
                        self.direction - self.determining_angle(
                            self.rect.centerx, self.rect.centery,
                            enemy.rect.centerx,
                            enemy.rect.centery)) >= 326:
                        if not enemy in characters_rendering:
                            characters_rendering.add(enemy)
                    else:
                        if enemy in characters_rendering:
                            characters_rendering.remove(enemy)
                else:
                    enemy.distance_beam = [False, False]
                    if enemy in characters_rendering:
                        characters_rendering.remove(enemy)
            else:
                enemy.distance_beam = [False, False]
                if enemy in characters_rendering:
                    characters_rendering.remove(enemy)

    def update(self):
        xshift = 0
        yshift = 0

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_w]:
            yshift -= 5
        if keystate[pygame.K_s]:
            yshift += 5
        if keystate[pygame.K_a]:
            xshift -= 5
        if keystate[pygame.K_d]:
            xshift += 5

            # поворот персонажа к курсору
        self.direction = self.determining_angle(self.rect.centerx,
                                                self.rect.centery,
                                                pygame.mouse.get_pos()[0],
                                                pygame.mouse.get_pos()[1])

        self.movement = False
        self.move_entity(xshift, yshift)
        self.wall_hitbox.x += xshift
        self.wall_hitbox.y += yshift
        self.visible_objects()





        if keystate[pygame.K_f]:
            nearest_door = self.get_nearest_door()
            door_dist_sq = (
                                   player.rect.centerx - nearest_door.rect.centerx) ** 2 + (
                                   player.rect.centery - nearest_door.rect.centery) ** 2 if nearest_door is not None else 1000000000
            min_dist = door_dist_sq
            if min_dist <= self.range:
                if min_dist == door_dist_sq:
                    if not nearest_door.is_open:  # дверь закрыта
                        nearest_door.use()
                    else:
                        if not pygame.Rect.colliderect(self.wall_hitbox,
                                                       nearest_door.rect):  # дверь открыта, но не пересекается с игроком
                            nearest_door.use()


        current_image = player_anim.get_current_image(
            *self.get_current_image_info())
        self.image = pygame.transform.rotate(current_image, self.direction + 90)
        self.rect = self.image.get_rect(center=self.rect.center)





class Wall(pygame.sprite.Sprite):
    """Класс стены"""

    def __init__(self, x, y):
        super().__init__(all_sprites, walls, walls_rendering)
        self.image = pygame.surface.Surface((50, 50))
        self.image.fill((128, 128, 128))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass


class Door(pygame.sprite.Sprite):
    """Класс двери"""

    def __init__(self, x, y, direction):
        super().__init__(all_sprites, doors, doors_wall, walls)
        self.direction = direction
        if direction == 0:
            self.image = door_textures[(1, 'vert')]
        elif direction == 1:
            self.image = door_textures[(1, 'hor')]
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.constx = x
        self.consty = y
        self.is_open = False
        self.max_delay = FPS
        self.delay = 0

    def use(self):
        if self.delay == 0:
            if self.is_open:
                if self.direction == 1:
                    wall_layout[(self.constx - 25) // 50][self.consty // 50][0] = True
                    wall_layout[(self.constx + 25) // 50][self.consty // 50][0] = True
                else:
                    wall_layout[self.constx // 50][(self.consty - 25) // 50][0] = True
                    wall_layout[self.constx // 50][(self.consty + 25) // 50][0] = True
                self.is_open = False
                walls.add(self)
                doors_wall.add(self)
            else:
                if self.direction == 1:
                    wall_layout[(self.constx - 25) // 50][self.consty // 50][0] = False
                    wall_layout[(self.constx + 25) // 50][self.consty // 50][0] = False
                else:
                    wall_layout[self.constx // 50][(self.consty - 25) // 50][0] = False
                    wall_layout[self.constx // 50][(self.consty + 25) // 50][0] = False
                self.is_open = True
                walls.remove(self)
                doors_wall.remove(self)
            self.delay = self.max_delay
            self.change_image()

    def change_image(self):
        self.image = self.get_current_image()

    def update(self):
        if self.delay != 0:
            self.delay -= 1
            self.change_image()

    def get_current_image(self):
        """Возвращает текущую текстуру двери"""
        orientation = 'hor' if self.direction == 1 else 'vert'
        if self.delay == 0:
            if self.is_open:
                frame = 6
            else:
                frame = 1
        elif self.delay == self.max_delay:
            if self.is_open:
                frame = 1
            else:
                frame = 6
        else:
            if self.is_open:
                frame = (self.max_delay - self.delay + 10) // (FPS // 6)
            else:
                frame = (self.delay + 10) // (FPS // 6)
        return door_textures[(frame, orientation)]


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy
        if type(obj) == Player:
            obj.wall_hitbox.x += self.dx
            obj.wall_hitbox.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class PlayerAnimation:
    def __init__(self):
        self.animations = \
            {'handgun': {
                'idle': [],
                'move': [],
                'reload': [],
                'shoot': []},
                'knife': {
                    'idle': [],
                    'shoot': [],
                    'move': []},
                'rifle': {
                    'idle': [],
                    'move': [],
                    'reload': [],
                    'shoot': []},
                'shotgun': {
                    'idle': [],
                    'move': [],
                    'reload': [],
                    'shoot': []}}
        for cdir, dirs, files in os.walk('assets/player_sprites'):
            for file in files:
                a1, a2 = cdir.split('\\')[1:]
                self.animations[a1][a2].append(
                    pygame.image.load(f'{cdir}\\{file}'))
        # print(self.animations)

    def get_current_image(self, weapon, state, frame_num):
        return self.animations[weapon][state][frame_num]


class EnemyAnimation:
    def __init__(self):
        self.animations = {'rifle': {
            'move': [],
            'shoot': []
        }}
        for cdir, dirs, files in os.walk('assets/enemy_sprites'):
            for file in files:
                a1, a2 = cdir.split('\\')[1:]
                self.animations[a1][a2].append(
                    pygame.image.load(f'{cdir}\\{file}'))

    def get_current_image(self, weapon, state, framenum):
        return self.animations[weapon][state][framenum]


class MapTexture(pygame.sprite.Sprite):
    """Текстуры карты"""

    def __init__(self):
        super().__init__(all_sprites, map_texture)
        self.image = map_image
        self.rect = self.image.get_rect()
        self.rect.topleft = -25, -25









if __name__ == '__main__':
    pygame.init()
    name = ''
    main_run = True


    while main_run:
        FPS = 60

        size = width, height = 1400, 700
        screen = pygame.display.set_mode(size, pygame.DOUBLEBUF, 32)
        clock = pygame.time.Clock()
        pygame.mouse.set_visible(True)  # False на релизе

        walls = pygame.sprite.Group()  # стены
        walls_rendering = pygame.sprite.Group()
        characters = pygame.sprite.Group()  # персонажи
        other_sprites = pygame.sprite.Group()  # все остальное
        all_sprites = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        lootboxes = pygame.sprite.Group()  # ящики
        enemies = pygame.sprite.Group()
        characters_rendering = pygame.sprite.Group()
        doors = pygame.sprite.Group()
        wall_boundaries = pygame.sprite.Group()
        doors_wall = pygame.sprite.Group()

        tiles = pygame.sprite.Group()
        furniture = pygame.sprite.Group()
        map_texture = pygame.sprite.Group()

        ammo_box_image = pygame.image.load('assets/ammo_box.png')
        sniper_rifle_image = pygame.image.load('assets/sniper_rifle2.png').convert()
        sniper_rifle_image.set_colorkey((255, 255, 255))
        ak_47_image = pygame.image.load('assets/ak_47_image2.png').convert()
        ak_47_image.set_colorkey((255, 255, 255))
        glock_image = pygame.image.load('assets/glock_image.png').convert()
        glock_image.set_colorkey((255, 255, 255))
        im1 = pygame.image.load('assets/Игрок_2.png').convert()
        im1.set_colorkey((255, 255, 255))
        knife_image = pygame.image.load('assets/knife_image.png').convert()
        knife_image.set_colorkey((255, 255, 255))
        shotgun_image = pygame.image.load('assets/shotgun_image.png').convert()
        shotgun_image.set_colorkey((255, 255, 255))
        medkit_image = pygame.image.load('assets/medkit.png').convert()

        im1 = pygame.image.load('1.png').convert()
        im1.set_colorkey((0, 0, 0))

        map_image = pygame.image.load('assets/map_100_texture.png')

        door_textures = {}
        for i in range(1, 7):
            for j in {'vert', 'hor'}:
                door_textures[(i, j)] = pygame.image.load(f'assets/door_textures/frame{i}_{j}.png')

        player_anim = PlayerAnimation()
        enemy_anim = EnemyAnimation()
        running = True

        camera = Camera()

        player = Player(4550, 4280)
        MapTexture()
        wall_layout = pic_to_map(
            'assets/map100.png')  # массив из пикселей картинки, где находится стена
        while running:
            # внутри игрового цикла ещё один цикл
            # приёма и обработки сообщений
            for event in pygame.event.get():
                # при закрытии окна
                if event.type == pygame.QUIT:
                    running = False
                    main_run = False
                # РЕАКЦИЯ НА ОСТАЛЬНЫЕ СОБЫТИЯ
            # отрисовка и изменение свойств объектов
            # characters.update()
            player.get_current_weapon().update()
            player.rect = player.image.get_rect(size=(64, 64),
                                                center=player.rect.center)
            player.update()
            for i in characters:
                if i != player:
                    i.update()
            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)
            screen.fill('black')
            map_texture.draw(screen)
            furniture.draw(screen)
            player.tracing()
            other_sprites.draw(screen)

            characters_rendering.draw(screen)

            other_sprites.draw(screen)
            doors.draw(screen)

            doors.update()
            for i in characters:
                i.rect = i.image.get_rect(size=(64, 64), center=i.rect.center)
            bullets.update()
            bullets.draw(screen)

            for lootbox in lootboxes:
                lootbox.draw_open_progress()

            screen.blit(
                pygame.font.Font(None, 30).render('Врагов осталось: ' + str(len(enemies)), True,
                                                  'red'), (50, 50))

            player.draw_interface()

            clock.tick(FPS)

            pygame.display.flip()

pygame.quit()
