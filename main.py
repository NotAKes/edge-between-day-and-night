import pygame
from dbreader import DBreader
import os
import time

# импорты

database = DBreader()


# обение с бд через этот класс

# функция для загрузки изображений
def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


# к./с.
FPS = 50
# грузим текстуры
tile_images = {
    'wall_dark': pygame.transform.scale(load_image('images/textures/tiles/black_tile.png'), (60, 60)),
    'wall_light': pygame.transform.scale(load_image('images/textures/tiles/white_tile.png'), (60, 60)),
    'wall_dark_red': pygame.transform.scale(load_image('images/textures/tiles/dark_red_tile.png'), (60, 60)),
    'wall_light_red': pygame.transform.scale(load_image('images/textures/tiles/light_red_tile.png'), (60, 60)),
    'wall_dark_green': pygame.transform.scale(load_image('images/textures/tiles/dark_green_tile.png'), (60, 60)),
    'wall_light_green': pygame.transform.scale(load_image('images/textures/tiles/light_green_tile.png'), (60, 60)),
    'black_cracked_wall':
        pygame.transform.scale(load_image('images/textures/tiles/black_tile_cracked.png'), (60, 60)),
    'white_cracked_wall':
        pygame.transform.scale(load_image('images/textures/tiles/white_tile_cracked.png'), (60, 60)),
    'dark_green_cracked_wall': pygame.transform.scale(load_image('images/textures/tiles/dark_green_tile_cracked.png'),
                                                      (60, 60)),
    'light_green_cracked_wall': pygame.transform.scale(load_image('images/textures/tiles/light_green_tile_cracked.png'),
                                                       (60, 60)),
    'dark_red_cracked_wall': pygame.transform.scale(load_image('images/textures/tiles/dark_red_tile_cracked.png'),
                                                    (60, 60)),
    'light_red_cracked_wall': pygame.transform.scale(load_image('images/textures/tiles/light_red_tile_cracked.png'),
                                                     (60, 60)),
    'empty': pygame.transform.scale(load_image('images/textures/tiles/road.png'), (60, 60)),
    'red_gem': pygame.transform.scale(load_image('images/textures/tiles/red_gem.png'), (60, 60)),
    'green_gem': pygame.transform.scale(load_image('images/textures/tiles/green_gem.png'), (60, 60)),
    'blue_gem': pygame.transform.scale(load_image('images/textures/tiles/blue_gem.png'), (60, 60))
}
# названия
gem_types = {'r': 'red_gem',
             'g': 'green_gem',
             'b': 'blue_gem'}
# размер клетки поля
tile_width = tile_height = 60


# главный класс окна
class Window:
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen
        self.layour_color = 'white'  # цвет бекграунда (меняется с цветом шрифта в change_color)
        self.font_color = 'black'  # цвет шрифта
        # грузим шрифты
        self.font_titles = pygame.font.Font('data/fonts/PixelCode-Bold.ttf', 39)
        self.font_regular = pygame.font.Font('data/fonts/PixelCode-DemiBold.ttf', 27)

    def change_color(self):
        self.layour_color, self.font_color = self.font_color, self.layour_color

    def render(self):
        pass


# окно при входе
class StartMenu(Window):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)
        self.width = width
        self.height = height
        self.screen = screen
        self.music_disc = load_image("images/music_disc.png")

    # рендерим надписи из шрифтов
    def render(self):
        self.title = self.font_titles.render('Colorless', True, self.font_color)
        ## TODO сделать запрос на трек
        self.music_label = self.font_regular.render('Clement Panchout - Jelly Blob', True, self.font_color)
        self.screen.fill(self.layour_color)
        self.screen.blit(self.title,
                         (self.width / 2 - self.title.get_width() / 2, 20))
        # выводим надписи
        self.screen.blit(self.music_disc, (10, 1150))
        self.screen.blit(self.music_label, (70, 1156))


# окно при победе
class VictoryWindow(Window):
    # получаем на вход текущий счет и лучший счёт
    def __init__(self, width, height, screen, score, best):
        super().__init__(width, height, screen)
        self.width = width
        self.height = height
        self.screen = screen
        self.score = score
        self.best_score = best

    # выводим надписи рекорды
    def render(self):
        self.title = self.font_titles.render('Colorless', True, self.font_color)
        self.gem_label = self.font_titles.render('Вы собрали самоцвет!', True, self.font_color)
        self.score_label = self.font_titles.render(f'Ваш счёт: {self.score}    Ваш лучший: {self.best_score} ', True,
                                                   self.font_color)
        self.screen.fill(self.layour_color)
        self.screen.blit(self.title,
                         (450, 20))
        self.screen.blit(self.gem_label, (350, 250))
        self.screen.blit(self.score_label, (250, 400))


# окно поражения
class LoseWindow(Window):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)
        self.width = width
        self.height = height
        self.screen = screen

    # выводим надписи
    def render(self):
        self.title = self.font_titles.render('Colorless', True, self.font_color)
        self.gem_label = self.font_titles.render('Время вышло!', True, self.font_color)
        self.screen.fill(self.layour_color)
        self.screen.blit(self.title,
                         (450, 20))
        self.screen.blit(self.gem_label, (440, 250))


# окно карты уровней
class LevelMenu(Window):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)
        # составляем строки из рекордов (из бд)
        self.black_best = f'Счёт: {str(database.get_best('black'))}'
        self.red_best = f'Счёт: {str(database.get_best('red'))}'
        self.green_best = f'Счёт: {str(database.get_best('green'))}'

    # выводим надписи и рекорды
    def render(self):
        self.title = self.font_titles.render('Карта', True, self.font_color)
        self.black_title = self.font_regular.render(self.black_best, True, self.font_color)
        self.red_title = self.font_regular.render(self.red_best, True, self.font_color)
        self.green_title = self.font_regular.render(self.green_best, True, self.font_color)
        self.screen.fill(self.layour_color)
        self.screen.blit(self.title, (self.width / 2 - self.title.get_width() / 2, 20))
        for num, i in enumerate([self.black_title, self.red_title, self.green_title]):
            self.screen.blit(i, (500 * (num * .84) + 130, 200))


# родительский класс уровня
class Level(Window):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)
        self.map_level = []  # здесь будет карта
        self.mode = 'd'  # режим на тёмный
        self.gem_type = 'r'  # цвет камня
        self.color = ''  # цвет уровня
        self.tile_empty = 'empty'  # название для пустой клетки
        self.wall_color = 'wall_black'  # название для клетки стены
        self.font_color = 'wall_white'  # название для клетки  при смене
        self.dark_cracked_wall = 'black_cracked_wall'  # название для проходной темной стены
        self.light_cracked_wall = 'white_cracked_wall'  # название для проходной светлой стены

    # подгружаем карту и записываем в  map_level
    def load_level(self, maps):
        level_map = [line.strip() for line in maps.split('\n')]
        max_width = max(map(len, level_map))
        self.map_level = list(map(lambda x: list(x.ljust(max_width, '.')), level_map))

    # смена цвета с wall_color на font_color и обратно
    def change_color(self):
        if self.mode == 'd':
            self.mode = 'l'
        else:
            self.mode = 'd'
        self.wall_color, self.font_color = self.font_color, self.wall_color
        # переписываем цвет на стенах
        for y in range(len(self.map_level)):
            for x in range(len(self.map_level[y])):
                if self.map_level[y][x] == '#':
                    Tile(self.wall_color, x, y)

    # чтение и генерация уровней по каждому символу
    def generate_level(self):
        new_player, x, y = None, None, None
        for y in range(len(self.map_level)):
            for x in range(len(self.map_level[y])):
                if self.map_level[y][x] == '.':
                    Tile(self.tile_empty, x, y)
                elif self.map_level[y][x] in 'rgb':
                    self.gem = GemTile(self.gem_type, x, y)
                elif self.map_level[y][x] == 'l':
                    Tile(self.dark_cracked_wall, x, y)
                elif self.map_level[y][x] == 'd':
                    Tile(self.light_cracked_wall, x, y)
                elif self.map_level[y][x] == '#':
                    Tile(self.wall_color, x, y)
                elif self.map_level[y][x] == '@':
                    Tile(self.tile_empty, x, y)
                    new_player = Player(x, y)
                    self.map_level[y][x] = "."

        return new_player, x, y


# дочерний класс черного уровня
class LevelBlack(Level):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)
        self.screen = screen
        self.color = 'black'
        self.tile_empty = 'empty'
        self.wall_color = 'wall_dark'
        self.font_color = 'wall_light'
        self.gem_type = 'r'
        self.level_name = database.get_black_map()  # получаем карту в бд
        self.load_level(self.level_name)

    def render(self):
        self.screen.fill(self.layour_color)


# дочерний класс красного уровня
class LevelRed(Level):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)
        self.screen = screen
        self.color = 'red'
        self.gem_type = 'g'
        self.tile_empty = 'empty'
        self.wall_color = 'wall_dark_red'
        self.font_color = 'wall_light_red'
        self.dark_cracked_wall = 'dark_red_cracked_wall'
        self.light_cracked_wall = 'light_red_cracked_wall'
        self.level_name = database.get_red_map()
        self.load_level(self.level_name)

    def render(self):
        self.screen.fill(self.layour_color)


# дочерний класс зеленого уровня
class LevelGreen(Level):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)
        self.screen = screen
        self.gem_type = 'b'
        self.color = 'green'
        self.tile_empty = 'empty'
        self.wall_color = 'wall_dark_green'
        self.font_color = 'wall_light_green'
        self.dark_cracked_wall = 'dark_green_cracked_wall'
        self.light_cracked_wall = 'light_green_cracked_wall'
        self.level_name = database.get_green_map()
        self.load_level(self.level_name)

    def render(self):
        self.screen.fill(self.layour_color)


# класс тайла (НЕ ГЕМ)
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(black_level_group, green_level_group, red_level_group)
        self.layour_color = 'black'
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)

    def update(self, font_color='white', layour_color='black', *args):
        self.layour_color = font_color


# класс гема (НЕ ТАЙЛ)
# Отдельный класс создан для того, чтобы упростить взаимодействие с игроком до коллайда по маске
class GemTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(black_level_group, green_level_group, red_level_group)
        self.tile_type = gem_types[tile_type]
        self.layour_color = 'black'
        print(self.tile_type)
        self.image = tile_images[self.tile_type]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)

    def update(self, font_color='white', layour_color='black', *args):
        self.layour_color = font_color


# класс игрока
class Player(pygame.sprite.Sprite):
    # подгружаем текстурку
    ghost = load_image(f"images/textures/player/ghost.png")

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        # рисуем, двигаем
        self.image = pygame.transform.scale(Player.ghost, (57, 57))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 2, tile_height * pos_y + 2)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = (pos_x, pos_y)

    # обрабатываем движение
    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * x + 2, tile_height * y + 2)
        self.pos = (x, y)


# класс бордера
class Border(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(border_group)
        self.walls_barrier = 0
        self.image = pygame.Surface([1200, 1200], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.draw()

    # рисуем 4 стены
    def draw(self):
        pygame.draw.rect(self.image, 'light gray', (0, 0, 1200, self.walls_barrier))
        pygame.draw.rect(self.image, 'light gray', (0, 1200 - self.walls_barrier, 1200, self.walls_barrier))
        pygame.draw.rect(self.image, 'light gray', (0, 0, self.walls_barrier, 1200))
        pygame.draw.rect(self.image, 'light gray', (1200 - self.walls_barrier, 0, self.walls_barrier, 1200))


# родительский класс кнопку
class Button(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.font_color = 'white'
        self.layour_color = 'black'
        self.text = ''
        # записываем в next_window окно, куда будет производится редирект по кнопке
        self.next_window = Window
        self.font_titles = pygame.font.Font('data/fonts/PixelCode-Bold.ttf', 39)
        self.font_regular = pygame.font.Font('data/fonts/PixelCode-DemiBold.ttf', 27)

    # функция для размера и расположения кнопок
    def get_image(self):
        self.image = pygame.Surface([0, 0])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    # отрисовка
    def draw(self):
        self.text_to_render = self.font_titles.render(self.text, True, self.font_color, self.layour_color)
        self.image.blit(self.text_to_render, self.text_to_render.get_rect())

    # обрабатываем нажатия и смены цвета, возращаем true и окно, если редирект, false, если нет
    def update(self, font_color='black', layour_color='white', *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            return [True, self.next_window]
        self.layour_color, self.font_color = layour_color, font_color
        self.draw()
        return [False]


# кнопка 'Начать игру'
class StartButton(Button):
    def __init__(self, *group):
        super().__init__(*group)
        self.text = 'Начать игру'
        self.get_image()
        self.next_window = LevelMenu

    def get_image(self):
        self.image = pygame.Surface([286, 53])
        self.rect = self.image.get_rect()
        self.rect.x = 450
        self.rect.y = 200
        self.draw()


# Кнопка из меню карты уровней назад
class BackToStart(Button):
    def __init__(self):
        super().__init__(level_menu_group)
        self.text = '⬅️'
        self.get_image()
        self.next_window = StartMenu

    def get_image(self):
        self.image = pygame.Surface([26, 45])
        self.rect = self.image.get_rect()
        self.rect.x = 40
        self.rect.y = 40
        self.draw()


# Кнопка вернуться в к уровням
class BackToLevelMenuButton(Button):
    def __init__(self):
        super().__init__(victory_group, lose_group)
        self.text = 'Вернуться в меню'
        self.get_image()
        self.next_window = LevelMenu

    def get_image(self):
        self.image = pygame.Surface([416, 45])
        self.rect = self.image.get_rect()
        self.rect.x = 370
        self.rect.y = 600
        self.draw()


# Кнопка попробовать уровень ещё раз
class RertyLevelButton(Button):
    def __init__(self, level):
        super().__init__(lose_group)
        self.text = 'Попробовать ещё раз'
        self.get_image()
        self.next_window = level

    def get_image(self):
        self.image = pygame.Surface([494, 46])
        self.rect = self.image.get_rect()
        self.rect.x = 350
        self.rect.y = 520
        self.draw()


# класс кнопки редирект на уровень
class LevelButton(Button):
    def __init__(self, number):
        super().__init__(level_menu_group)
        self.number = number
        self.text = f'Level {number}'
        self.get_image()
        # по номеру кнопки определяем следующий уровень
        if self.number == 1:
            self.next_window = LevelBlack
        elif self.number == 2:
            self.next_window = LevelRed
        else:
            self.next_window = LevelGreen

    def get_image(self):
        self.image = pygame.Surface([182, 43])
        self.rect = self.image.get_rect()
        self.rect.x = 120 + 422 * (self.number - 1)
        self.rect.y = 140
        self.draw()


# Отдельная кнопка для управлением звука
class SoundButton(pygame.sprite.Sprite):
    # грузим изображения
    sound_on_white = load_image(f"images/sound_on_white.png")
    sound_on_black = load_image(f"images/sound_on_black.png")
    sound_off_white = load_image(f"images/sound_off_white.png")
    sound_off_black = load_image(f"images/sound_off_black.png")

    def __init__(self):
        super().__init__(main_menu_group)
        # грузим статус и цвет
        self.color = 'white'
        self.status = 'on'
        self.image = SoundButton.sound_on_white
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 600

    # обновляем цвета и статусы после нажатий
    def update(self, font_color, layout_color, *args):
        self.color = font_color
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            if self.status == 'on':
                self.status = 'off'
            else:
                self.status = 'on'
        self.image = load_image(f"images/sound_{self.status}_{self.color}.png")


class DecorativeGhost(pygame.sprite.Sprite):
    # подгружаем текстурку
    ghost = load_image(f"images/textures/player/ghost.png")

    def __init__(self):
        super().__init__(main_menu_group, level_menu_group, lose_group, victory_group)
        # рисуем, двигаем
        self.pos_x = 1
        self.pos_y = 462
        self.direction = 1
        self.image = pygame.transform.scale(DecorativeGhost.ghost, (57, 57))
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)

    def update(self, font_color, layout_color, *args):
        # если у края, то меняем текстурку и направление
        if self.pos_x > 1150 or self.pos_x <= 0:
            self.direction *= (-1)
            self.image = pygame.transform.flip(self.image, True, False)
        self.pos_x += 2 * self.direction
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)


# Таймер для счёта
class Timer:
    def __init__(self):
        self.start = time.perf_counter()

    # рестарт
    def restart(self):
        self.start = time.perf_counter()

    # получаем время
    def get_time(self):
        return round(time.perf_counter() - self.start)


# создаем группы спрайтов
main_menu_group = pygame.sprite.Group()
border_group = pygame.sprite.Group()
level_menu_group = pygame.sprite.Group()
black_level_group = pygame.sprite.Group()
red_level_group = pygame.sprite.Group()
map_level_group = pygame.sprite.Group()
green_level_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
victory_group = pygame.sprite.Group()
lose_group = pygame.sprite.Group()
# словарь для групп и кнопок
groups_dict = {StartMenu: main_menu_group,
               LevelMenu: level_menu_group,
               LevelRed: red_level_group,
               LevelGreen: green_level_group,
               LevelBlack: black_level_group}


# метод обработки движений
def move(hero, movement, map, mode):
    x, y = hero.pos  # записываем позицию
    # если движение возможно, то двигаемся
    if movement == "up":
        if y > 0 and (map[y - 1][x] in f'.rgb{mode}'):
            hero.move(x, y - 1)
    elif movement == "down":
        if y < 1200 and (map[y + 1][x] in f'.rgb{mode}'):
            hero.move(x, y + 1)
    elif movement == "left":
        if x > 0 and (map[y][x - 1] in f'.rgb{mode}'):
            hero.move(x - 1, y)
    elif movement == "right":
        if x < 1200 and (map[y][x + 1] in f'.rgb{mode}'):
            hero.move(x + 1, y)


# инициализация и основной цикл
if __name__ == '__main__':
    pygame.init()
    # окно
    size = width, height = 1200, 1200
    screen = pygame.display.set_mode(size)
    # название
    pygame.display.set_caption('Colorless')
    # часы
    clock = pygame.time.Clock()
    time_on = False
    # бордер и евент бордера
    walls_barrier = 0
    walls_visible_event = pygame.USEREVENT + 1
    pygame.time.set_timer(walls_visible_event, 300)
    #  кнопки уровней
    for i in range(1, 4):
        LevelButton(i)
    sound_button = SoundButton() # кнопка звука
    endgame_event = None  # евент для конца игры
    # создаем стартовое окно и группу
    current_window = previous_window = StartMenu(width, height, screen)
    current_group = previous_group = main_menu_group
    # задаток бордера
    border = None
    # добавляем кнопки
    DecorativeGhost()
    StartButton(main_menu_group)
    BackToStart()
    BackToLevelMenuButton()
    RertyLevelButton(LevelBlack)
    # рендерим окно и запускаем цикл
    current_window.render()
    running = True
    # создаем музыку
    pygame.mixer.init()
    main_channel = pygame.mixer.Channel(0)
    status_channel = pygame.mixer.Channel(1)
    music_menu = pygame.mixer.Sound('data/music/music.wav')
    music_level = pygame.mixer.Sound('data/music/level.wav')
    win_sound = pygame.mixer.Sound('data/music/win.wav')
    lose_sound = pygame.mixer.Sound('data/music/lose.wav')
    music_menu.set_volume(0.1)
    music_level.set_volume(0.1)
    win_sound.set_volume(0.3)
    lose_sound.set_volume(0.3)
    main_channel.play(music_menu, loops=-1)
    # цикл
    while running:
        # записываем всё кликабельное
        changeable_buttons = [i for i in current_group.sprites() if isinstance(i, Button)]
        # включаем и выключаем музыку
        if sound_button.status == 'off':
            main_channel.pause()
        else:
            main_channel.unpause()
        # обработки евентов
        for event in pygame.event.get():
            # выход
            if event.type == pygame.QUIT:
                running = False
            # если бордер есть, то прибавляем его
            if event.type == walls_visible_event and border:
                border.walls_barrier += 1
                border.draw()
            # если нажата ЛКМ
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                coords = event.pos
                # если нажали кнопку
                for sprite in changeable_buttons:
                    # редиректим && апдейтим
                    if sprite.update('white', 'white', event)[0]:
                        previous_window = current_window
                        current_window = sprite.update('', '', event)[1](width, height, screen)
                        previous_group, current_group = current_group, groups_dict[type(current_window)]
                        changeable_buttons = [i for i in current_group.sprites() if isinstance(i, Button)]
                        current_window.render()
                    current_group.update(current_window.font_color, current_window.layour_color, event)
            # сменяем цвет по нажатию на е
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                current_window.change_color()
                current_group.update(current_window.font_color, current_window.layour_color, event)
                current_window.render()
            # обрабатываем возвраты на еск
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and previous_window != current_window:
                current_window, current_group = previous_window, previous_group
                current_window.render()
                current_group.update(current_window.font_color, current_window.layour_color, event)
            # если мы на уровне + есть нажатия кнопок движения, то двигаемся
            if event.type == pygame.KEYDOWN and isinstance(current_window, Level):
                if event.key == pygame.K_UP:
                    move(player_group.sprites()[0], "up", current_window.map_level, current_window.mode)
                elif event.key == pygame.K_DOWN:
                    move(player_group.sprites()[0], "down", current_window.map_level, current_window.mode)
                elif event.key == pygame.K_LEFT:
                    move(player_group.sprites()[0], "left", current_window.map_level, current_window.mode)
                elif event.key == pygame.K_RIGHT:
                    move(player_group.sprites()[0], "right", current_window.map_level, current_window.mode)
            # если время вышло и сейчас уровень
            if endgame_event and event.type == endgame_event and isinstance(current_window, Level):
                current_window = LoseWindow(width, height, screen)
                current_group = lose_group
                status_channel.play(lose_sound)
                current_group.update(current_window.font_color, current_window.layour_color, event)
                current_window.render()
        # апдейтим группы
        current_window.render()
        current_group.update(current_window.font_color, current_window.layour_color)
        current_group.draw(screen)


        # если сейчас уровень и группы есть, то рисуем их
        if player_group and isinstance(current_window, Level):
            player_group.draw(screen)
            border_group.draw(screen)
            # если персонаж коллайдит с гемом, то победа
            if pygame.sprite.collide_mask(player_group.sprites()[0], current_window.gem):
                database.check_best(timer.get_time(), current_window.color)
                current_window = VictoryWindow(width, height, screen, timer.get_time(),
                                               database.get_best(current_window.color))
                current_group = victory_group
                status_channel.play(win_sound)
                current_group.update(current_window.font_color, current_window.layour_color, event)
                current_window.render()
        # если группы нет, то создаем уровень и границы + музыка
        elif isinstance(current_window, Level):
            current_window.generate_level()
            border = Border()
            main_channel.play(music_level, loops=-1)
            endgame_event = pygame.USEREVENT + 2
            pygame.time.set_timer(endgame_event, 60 * 3 * 1000)
            timer = Timer()
        # условие для выхода. Группы удаляем
        elif player_group:
            main_channel.play(music_menu, loops=-1)
            player_group.sprites()[0].kill()
            border_group.sprites()[0].kill()
        # апдейт и тикаем
        pygame.display.update()
        clock.tick(FPS)
    # выход
    pygame.quit()
