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


pygame.init()
screen_size = (400, 400)
screen = pygame.display.set_mode(screen_size)
FPS = 50

tile_images = {
    'wall': pygame.transform.scale(load_image('images/textures/black_tile.png'), (80, 80)),
    'empty': pygame.transform.scale(load_image('images/textures/grass.png'), (80, 80))
}

tile_width = tile_height = 80


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
        pygame.display.update()


class PauseMenu(Window):
    pass


class Level(Window):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)
        self.current_checkpoint = 0
        self.map_level = []
        self.level_name = ''

    def load_level(self, maps):
        level_map = [line.strip() for line in maps.split('\n')]
        max_width = max(map(len, level_map))
        self.map_level = list(map(lambda x: list(x.ljust(max_width, '.')), level_map))

    # чтение и генерация уровней
    def generate_level(self):
        new_player, x, y = None, None, None
        for y in range(len(self.map_level)):
            for x in range(len(self.map_level[y])):
                if self.map_level[y][x] == '.':
                    Tile('empty', x, y)
                elif self.map_level[y][x] == '#':
                    Tile('wall', x, y)
                elif self.map_level[y][x] == '@':
                    Tile('empty', x, y)
                    new_player = Player(x, y)
                    self.map_level[y][x] = "."
        return new_player, x, y


class LevelBlack(Level):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)
        self.screen = screen
        self.level_name = database.get_black_map()
        self.load_level(self.level_name)

    def render(self):
        self.screen.fill(self.layour_color)


class LevelRed(Level):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)
        print('red')
        self.layour_color = 'pink'
        self.font_color = 'dark red'

    def render(self):
        self.screen.fill(self.layour_color)


class LevelGreen(Level):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)
        print('green')
        self.layour_color = 'light green'
        self.font_color = 'dark green'

    def render(self):
        self.screen.fill(self.layour_color)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(black_level_group, green_level_group, red_level_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)


class Player(pygame.sprite.Sprite):
    ghost = load_image(f"images/textures/player/ghost.png")

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = pygame.transform.scale(Player.ghost, (72, 72))
        self.pos = (pos_x, pos_y)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 5, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        camera.dx -= tile_width * (x - self.pos[0])
        camera.dy -= tile_height * (y - self.pos[1])
        self.pos = (x, y)
        for sprite in black_level_group:
            camera.apply(sprite)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x = obj.abs_pos[0] + self.dx
        obj.rect.y = obj.abs_pos[1] + self.dy

    def update(self, target):
        self.dx = 0
        self.dy = 0


# class PlayerBar(pygame.sprite.Sprite):
#     no_heart = load_image(f"images/textures/player/no_heart.png")
#     white_heart = load_image(f"images/textures/player/white_heart.png")
#     black_heart = load_image(f"images/textures/player/black_heart.png")
#     red_heart = load_image(f"images/textures/player/red_heart.png")
#
#     def __init__(self, number, *group):
#         super().__init__(*group)
#
#         self.image = pygame.transform.scale(PlayerBar.black_heart, (64, 64))
#         self.rect = self.image.get_rect()
#         self.rect.x = 20 + 75 * number
#         self.rect.y = 5
#         self.is_active = True
#
#     def update(self, font_color, layour_color, *args):
#         if not self.is_active:
#             self.image = pygame.transform.scale(PlayerBar.no_heart, (64, 64))
#             return
#
#         if layour_color in ['black', 'dark red', 'dark green']:
#             self.image = pygame.transform.scale(PlayerBar.white_heart, (64, 64))
#         else:
#             self.image = pygame.transform.scale(PlayerBar.black_heart, (64, 64))


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


def move(hero, movement, map):
    # FIXME

    x, y = hero.pos
    if movement == "up":
        if y > 0 and map[y - 1][x] == ".":
            hero.move(x, y - 1)
    elif movement == "down":
        if y < 700 - 1 and map[y + 1][x] == ".":
            hero.move(x, y + 1)
    elif movement == "left":
        if x > 0 and map[y][x - 1] == ".":
            hero.move(x - 1, y)
    elif movement == "right":
        if x < 1000 - 1 and map[y][x + 1] == ".":
            hero.move(x + 1, y)


if __name__ == '__main__':
    pygame.init()
    camera = Camera()
    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Colorless')
    clock = pygame.time.Clock()
    time_on = False
    ticks = 0

    for i in range(1, 4):
        LevelBtn(i, level_menu_group)
    SoundButton(main_menu_group, level_menu_group)

    current_window = previous_window = StartMenu(width, height, screen)
    current_group = previous_group = main_menu_group

    StartButton(main_menu_group)
    current_window.render()
    running = True
    f = 0
    while running:
        changeable_buttons = [i for i in current_group.sprites() if isinstance(i, Button)]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
                    move(player_group.sprites()[0], "up", current_window.map_level)
                elif event.key == pygame.K_DOWN:
                    move(player_group.sprites()[0], "down", current_window.map_level)
                elif event.key == pygame.K_LEFT:
                    move(player_group.sprites()[0], "left", current_window.map_level)
                elif event.key == pygame.K_RIGHT:
                    move(player_group.sprites()[0], "right", current_window.map_level)

        current_group.update(current_window.font_color, current_window.layour_color)
        current_group.draw(screen)
        if player_group:
            player_group.draw(screen)
        elif isinstance(current_window, Level):
            current_window.generate_level()

        pygame.display.update()
        clock.tick(FPS)
        ticks += 1
    pygame.quit()
