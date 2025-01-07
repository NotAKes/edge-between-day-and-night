import pygame
from dbreader import DBreader


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
        self.music_disc = pygame.image.load("data/images/music_disc.png")
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


class LevelBlack(Level):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)
        self.screen = screen

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


class Player(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.Surface((40, 60))
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = 500
        self.velocity = 4
        self.hearts_remain = 2

    def update(self, font_color, layour_color, *args):
        if layour_color in ['black', 'dark red', 'dark green']:
            self.image.fill('light blue')
        else:
            self.image.fill('blue')

    def drop_shadow(self):
        shadow_offset = (self.rect.x + 10, self.rect.y + 10)
        pygame.draw.rect(screen, 'dark blue', (shadow_offset[0], shadow_offset[1], self.rect.width, self.rect.height))


class PlayerBar(pygame.sprite.Sprite):
    white_heart = pygame.image.load(f"data/images/textures/player/white_heart.png")
    black_heart = pygame.image.load(f"data/images/textures/player/black_heart.png")
    red_heart = pygame.image.load(f"data/images/textures/player/red_heart.png")

    def __init__(self,number ,*group):
        super().__init__(*group)

        self.image = pygame.transform.scale(PlayerBar.black_heart, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.x = 20 + 75 * number
        self.rect.y = 5
        self.is_active = True


    def update(self, font_color, layour_color, *args):

        if layour_color in ['black', 'dark red', 'dark green']:
            self.image = pygame.transform.scale(PlayerBar.white_heart, (64, 64))
        else:
            self.image = pygame.transform.scale(PlayerBar.black_heart, (64, 64))

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
    sound_on_white = pygame.image.load(f"data/images/sound_on_white.png")
    sound_on_black = pygame.image.load(f"data/images/sound_on_black.png")
    sound_off_white = pygame.image.load(f"data/images/sound_off_white.png")
    sound_off_black = pygame.image.load(f"data/images/sound_off_black.png")

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
        self.image = pygame.image.load(f"data/images/sound_{self.status}_{self.color}.png")


main_menu_group = pygame.sprite.Group()
level_menu_group = pygame.sprite.Group()
pause_menu_group = pygame.sprite.Group()
black_level_group = pygame.sprite.Group()
red_level_group = pygame.sprite.Group()
green_level_group = pygame.sprite.Group()
groups_dict = {StartMenu: main_menu_group,
               LevelMenu: level_menu_group,
               PauseMenu: pause_menu_group,
               LevelRed: red_level_group,
               LevelGreen: green_level_group,
               LevelBlack: black_level_group}

if __name__ == '__main__':
    pygame.init()
    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('The Edge Between Day And Night')
    clock = pygame.time.Clock()
    time_on = False
    ticks = 0

    for i in range(1, 4):
        LevelBtn(i, level_menu_group)
    SoundButton(main_menu_group, level_menu_group)
    player = Player(black_level_group, green_level_group, red_level_group)

    current_window = previous_window = StartMenu(width, height, screen)
    current_group = previous_group = main_menu_group

    StartButton(main_menu_group)
    current_window.render()
    running = True
    while running:
        for i in range(player.hearts_remain):
            PlayerBar(i, black_level_group, green_level_group, red_level_group)
        current_group.update(current_window.font_color, current_window.layour_color)
        current_group.draw(screen)
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

            if any(pygame.key.get_pressed()) and isinstance(current_window, Level):
                if pygame.key.get_pressed()[pygame.K_a]:
                    player.rect.x -= player.velocity
                if pygame.key.get_pressed()[pygame.K_d]:
                    player.rect.x += player.velocity
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    for i in range(1, player.velocity * 2 + 1):
                        if i <= (player.velocity * 2 + 1) // 2:
                            player.rect.y -= (player.velocity ** 2) * 5
                        else:
                            player.rect.y += (player.velocity ** 2) * 5
                        pygame.time.delay(40)
                        current_window.render()
                        current_group.draw(screen)
                        pygame.display.update()

                current_window.render()
                current_group.draw(screen)

        pygame.display.update()
        clock.tick(60)
        ticks += 1
    pygame.quit()
