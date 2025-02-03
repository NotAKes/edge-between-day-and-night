import pygame
from dbreader import DBreader
import os
import sys

database = DBreader()


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


FPS = 50

tile_images = {
    'wall_dark': pygame.transform.scale(load_image('images/textures/tiles/black_tile.png'), (60, 60)),
    'wall_light': pygame.transform.scale(load_image('images/textures/tiles/white_tile.png'), (60, 60)),
    'wall_dark_red': pygame.transform.scale(load_image('images/textures/tiles/dark_red_tile.png'), (60, 60)),
    'wall_light_red': pygame.transform.scale(load_image('images/textures/tiles/light_red_tile.png'), (60, 60)),
    'wall_dark_green': pygame.transform.scale(load_image('images/textures/tiles/dark_green_tile.png'), (60, 60)),
    'wall_light_green': pygame.transform.scale(load_image('images/textures/tiles/light_green_tile.png'), (60, 60)),
    'black_cracked_wall': pygame.transform.scale(load_image('images/textures/tiles/black_tile_cracked.png'), (60, 60)),
    'white_cracked_wall': pygame.transform.scale(load_image('images/textures/tiles/white_tile_cracked.png'), (60, 60)),
    'dark_green_cracked_wall': pygame.transform.scale(load_image('images/textures/tiles/dark_green_tile_cracked.png'),
                                                      (60, 60)),
    'light_green_cracked_wall': pygame.transform.scale(load_image('images/textures/tiles/light_green_tile_cracked.png'),
                                                       (60, 60)),
    'dark_red_cracked_wall': pygame.transform.scale(load_image('images/textures/tiles/dark_red_tile_cracked.png'),
                                                    (60, 60)),
    'light_red_cracked_wall': pygame.transform.scale(load_image('images/textures/tiles/light_red_tile_cracked.png'),
                                                     (60, 60)),
    'empty': pygame.transform.scale(load_image('images/textures/grass.png'), (60, 60))
}
tile_width = tile_height = 60


class Window:
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen
        self.layour_color = 'white'
        self.font_color = 'black'
        self.font_titles = pygame.font.Font('data/fonts/PixelCode-Bold.ttf', 39)
        self.font_regular = pygame.font.Font('data/fonts/PixelCode-DemiBold.ttf', 27)

    def change_color(self):
        self.layour_color, self.font_color = self.font_color, self.layour_color

    def render(self):
        print('works!')


class StartMenu(Window):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)
        self.width = width
        self.height = height
        self.screen = screen

    def render(self):
        self.title = self.font_titles.render('Colorless', True, self.font_color)
        self.music_disc = load_image("images/music_disc.png")
        ## TODO сделать запрос на трек
        self.music_label = self.font_regular.render('Track_Title - Author', True, self.font_color)
        self.screen.fill(self.layour_color)
        self.screen.blit(self.title,
                         (self.width / 2 - self.title.get_width() / 2, 20))
        self.screen.blit(self.music_disc, (10, 650))
        self.screen.blit(self.music_label, (70, 656))
        pygame.display.update()


class LevelMenu(Window):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)

    def render(self):
        self.title = self.font_titles.render('Level map', True, self.font_color)
        self.screen.fill(self.layour_color)
        self.screen.blit(self.title, (self.width / 2 - self.title.get_width() / 2, 20))


class PauseMenu(Window):
    pass


class Level(Window):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)
        self.current_checkpoint = 0
        self.map_level = []
        self.level_name = ''
        self.mode = 'd'
        self.tile_empty = 'empty'
        self.wall_color = 'wall_black'
        self.font_color = 'wall_white'
        self.dark_cracked_wall = 'black_cracked_wall'
        self.light_cracked_wall = 'white_cracked_wall'

    def load_level(self, maps):
        level_map = [line.strip() for line in maps.split('\n')]
        max_width = max(map(len, level_map))
        self.map_level = list(map(lambda x: list(x.ljust(max_width, '.')), level_map))

    def change_color(self):
        # TODO доделать
        if self.mode == 'd':
            self.mode = 'l'
        else:
            self.mode = 'd'
        self.wall_color, self.font_color = self.font_color, self.wall_color
        for y in range(len(self.map_level)):
            for x in range(len(self.map_level[y])):
                if self.map_level[y][x] == '#':
                    Tile(self.wall_color, x, y)

    # чтение и генерация уровней
    def generate_level(self):
        new_player, x, y = None, None, None
        for y in range(len(self.map_level)):
            for x in range(len(self.map_level[y])):
                if self.map_level[y][x] == '.':
                    Tile(self.tile_empty, x, y)
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


class LevelBlack(Level):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)
        self.screen = screen
        self.tile_empty = 'empty'
        self.wall_color = 'wall_dark'
        self.font_color = 'wall_light'

        self.level_name = database.get_black_map()
        self.load_level(self.level_name)

    def render(self):
        self.screen.fill(self.layour_color)


class LevelRed(Level):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)
        self.screen = screen

        self.tile_empty = 'empty'
        self.wall_color = 'wall_dark_red'
        self.font_color = 'wall_light_red'
        self.dark_cracked_wall = 'dark_red_cracked_wall'
        self.light_cracked_wall = 'light_red_cracked_wall'

        self.level_name = database.get_black_map()
        self.load_level(self.level_name)

    def render(self):
        self.screen.fill(self.layour_color)


class LevelGreen(Level):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)
        self.screen = screen

        self.tile_empty = 'empty'
        self.wall_color = 'wall_dark_green'
        self.font_color = 'wall_light_green'
        self.dark_cracked_wall = 'dark_green_cracked_wall'
        self.light_cracked_wall = 'light_green_cracked_wall'
        self.level_name = database.get_black_map()
        self.load_level(self.level_name)

    def render(self):
        self.screen.fill(self.layour_color)


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


class Player(pygame.sprite.Sprite):
    ghost = load_image(f"images/textures/player/ghost.png")

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = pygame.transform.scale(Player.ghost, (57, 57))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 2, tile_height * pos_y + 2)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * x + 2, tile_height * y + 2)
        self.pos = (x, y)


class Border(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(border_group)
        self.walls_barrier = 0
        self.image = pygame.Surface([1200, 1200], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.draw()

    def draw(self):
        pygame.draw.rect(self.image, 'yellow', (0, 0, 1200, self.walls_barrier))
        pygame.draw.rect(self.image, 'yellow', (0, 1200 - self.walls_barrier, 1200, self.walls_barrier))
        pygame.draw.rect(self.image, 'yellow', (0, 0, self.walls_barrier, 1200))
        pygame.draw.rect(self.image, 'yellow', (1200 - self.walls_barrier, 0, self.walls_barrier, 1200))


class Button(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.font_color = 'white'
        self.layour_color = 'black'
        self.text = ''
        self.next_window = Window
        self.font_titles = pygame.font.Font('data/fonts/PixelCode-Bold.ttf', 39)
        self.font_regular = pygame.font.Font('data/fonts/PixelCode-DemiBold.ttf', 27)

    def get_image(self):
        self.image = pygame.Surface([0, 0])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def draw(self):
        self.text_to_render = self.font_titles.render(self.text, True, self.font_color, self.layour_color)
        self.image.blit(self.text_to_render, self.text_to_render.get_rect())

    def update(self, font_color='black', layour_color='white', *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            return [True, self.next_window]
        self.layour_color, self.font_color = layour_color, font_color
        self.draw()
        return [False]


class StartButton(Button):
    def __init__(self, *group):
        super().__init__(*group)
        self.text = 'Start Game'
        self.get_image()
        self.next_window = LevelMenu

    def get_image(self):
        self.image = pygame.Surface([260, 43])
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 200
        self.draw()


class LevelBtn(Button):
    def __init__(self, number, *group):
        super().__init__(*group)
        self.number = number
        self.text = f'Level {number}'
        self.get_image()
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


class SoundButton(pygame.sprite.Sprite):
    sound_on_white = load_image(f"images/sound_on_white.png")
    sound_on_black = load_image(f"images/sound_on_black.png")
    sound_off_white = load_image(f"images/sound_off_white.png")
    sound_off_black = load_image(f"images/sound_off_black.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.color = 'white'
        self.status = 'on'
        self.image = SoundButton.sound_on_white
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 600

    def update(self, font_color, layout_color, *args):
        self.color = font_color
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            if self.status == 'on':
                self.status = 'off'
            else:
                self.status = 'on'
        self.image = load_image(f"images/sound_{self.status}_{self.color}.png")


main_menu_group = pygame.sprite.Group()
border_group = pygame.sprite.Group()
level_menu_group = pygame.sprite.Group()
pause_menu_group = pygame.sprite.Group()
black_level_group = pygame.sprite.Group()
red_level_group = pygame.sprite.Group()
map_level_group = pygame.sprite.Group()
green_level_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
groups_dict = {StartMenu: main_menu_group,
               LevelMenu: level_menu_group,
               PauseMenu: pause_menu_group,
               LevelRed: red_level_group,
               LevelGreen: green_level_group,
               LevelBlack: black_level_group}


def move(hero, movement, map, mode):
    x, y = hero.pos
    if movement == "up":
        if y > 0 and (map[y - 1][x] == "." or map[y - 1][x] == mode):
            hero.move(x, y - 1)
    elif movement == "down":
        # fixme ymax and xmax
        if y < 1200 and (map[y + 1][x] == "." or map[y + 1][x] == mode):
            hero.move(x, y + 1)
    elif movement == "left":
        if x > 0 and (map[y][x - 1] == "." or map[y][x - 1] == mode):
            hero.move(x - 1, y)
    elif movement == "right":
        if x < 1200 and (map[y][x + 1] == "." or map[y][x + 1] == mode):
            hero.move(x + 1, y)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1200, 1200
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Colorless')
    clock = pygame.time.Clock()
    time_on = False
    walls_barrier = 0
    walls_visible = pygame.USEREVENT + 25
    pygame.time.set_timer(walls_visible, 300)

    for i in range(1, 4):
        LevelBtn(i, level_menu_group)
    SoundButton(main_menu_group, level_menu_group)

    current_window = previous_window = StartMenu(width, height, screen)
    current_group = previous_group = main_menu_group
    border = None
    StartButton(main_menu_group)
    current_window.render()
    running = True
    f = 0
    while running:
        changeable_buttons = [i for i in current_group.sprites() if isinstance(i, Button)]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == walls_visible and border:
                border.walls_barrier += 1
                border.draw()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                coords = event.pos
                # FIXME
                for sprite in changeable_buttons:

                    if sprite.update('white', 'white', event)[0]:
                        previous_window = current_window
                        current_window = sprite.update('', '', event)[1](width, height, screen)
                        previous_group, current_group = current_group, groups_dict[type(current_window)]
                        changeable_buttons = [i for i in current_group.sprites() if isinstance(i, Button)]
                        current_window.render()
                    current_group.update(current_window.font_color, current_window.layour_color, event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                current_window.change_color()
                current_group.update(current_window.font_color, current_window.layour_color, event)
                current_window.render()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and previous_window != current_window:
                current_window, current_group = previous_window, previous_group
                current_window.render()
                current_group.update(current_window.font_color, current_window.layour_color, event)

            if event.type == pygame.KEYDOWN and isinstance(current_window, Level):
                if event.key == pygame.K_UP:
                    move(player_group.sprites()[0], "up", current_window.map_level, current_window.mode)
                elif event.key == pygame.K_DOWN:
                    move(player_group.sprites()[0], "down", current_window.map_level, current_window.mode)
                elif event.key == pygame.K_LEFT:
                    move(player_group.sprites()[0], "left", current_window.map_level, current_window.mode)
                elif event.key == pygame.K_RIGHT:
                    move(player_group.sprites()[0], "right", current_window.map_level, current_window.mode)

        current_group.update(current_window.font_color, current_window.layour_color)
        current_group.draw(screen)

        if player_group and isinstance(current_window, Level):
            player_group.draw(screen)
            border_group.draw(screen)
        elif isinstance(current_window, Level):
            current_window.generate_level()
            border = Border()
        elif player_group:
            player_group.sprites()[0].kill()
            border_group.sprites()[0].kill()

        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
