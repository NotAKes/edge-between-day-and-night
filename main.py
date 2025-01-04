import pygame
from dbreader import DBreader


class Window:
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen
        self.layour_color = 'black'
        self.font_color = 'white'
        self.font_titles = pygame.font.Font('data/fonts/PixelCode-Bold.ttf', 33)
        self.font_regular = pygame.font.Font('data/fonts/PixelCode-DemiBold.ttf', 22)

    def change_color(self):
        self.layour_color, self.font_color = self.font_color, self.layour_color


class Button(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.font_color = 'white'
        self.layour_color = 'black'
        self.text = ''
        self.font_titles = pygame.font.Font('data/fonts/PixelCode-Bold.ttf', 33)
        self.font_regular = pygame.font.Font('data/fonts/PixelCode-DemiBold.ttf', 22)

    def get_image(self):
        self.image = pygame.Surface([0, 0])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def draw(self):
        self.text_to_render = self.font_titles.render(self.text, True, self.font_color, self.layour_color)
        self.image.blit(self.text_to_render, self.text_to_render.get_rect())

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            return True
        if args and args[0].type == pygame.KEYDOWN and event.key == pygame.K_e:
            self.layour_color, self.font_color = self.font_color, self.layour_color
        self.draw()


class StartButton(Button):
    def __init__(self, *group):
        super().__init__(*group)
        self.text = 'Start Game'
        self.get_image()

    def get_image(self):
        self.image = pygame.Surface([220, 43])
        self.rect = self.image.get_rect()
        self.rect.x = 330
        self.rect.y = 200
        self.draw()


class LevelBtn(Button):
    def __init__(self, number ,*group):
        super().__init__(*group)
        self.number = number
        print(self.number)
        self.text = f'Level {number}'
        self.get_image()

    def get_image(self):
        self.image = pygame.Surface([154, 43])
        self.rect = self.image.get_rect()
        self.rect.x = 120 + 250 * (self.number - 1)
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
        self.rect.y = 500

    def update(self, *args):
        if args and args[0].type == pygame.KEYDOWN and event.key == pygame.K_e:
            if self.color == 'white':
                self.color = 'black'
            else:
                self.color = 'white'
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            if self.status == 'on':
                self.status = 'off'
            else:
                self.status = 'on'
        self.image = pygame.image.load(f"data/images/sound_{self.status}_{self.color}.png")


class StartMenu(Window):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)

    def render(self):
        self.title = self.font_titles.render('The Edge Between Day And Night', True, self.font_color)
        self.music_disc = pygame.image.load("data/images/music_disc.png")
        ## TODO сделать запрос на трек
        self.music_label = self.font_regular.render('Track_Title - Author', True, self.font_color)
        self.screen.fill(self.layour_color)
        self.screen.blit(self.title,
                         (self.width / 2 - self.title.get_width() / 2, 20))
        self.screen.blit(self.music_disc, (10, 550))
        self.screen.blit(self.music_label, (70, 556))
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


class Level:
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen
        self.layour_color = 'black'
        self.font_color = 'white'
        self.font = pygame.font.Font(None, 40)
        self.current_checkpoint = 0


class LevelBlack(Level):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)


class LevelRed(Level):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)


class LevelGreen(Level):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)


status_dict = {StartMenu: 'main_menu',
               LevelMenu: 'level_menu',
               LevelRed: 'red',
               LevelGreen: 'green',
               LevelBlack: 'black'}

main_menu_group = pygame.sprite.Group()
level_menu_group = pygame.sprite.Group()

status = 'main_menu'
if __name__ == '__main__':
    pygame.init()
    size = width, height = 900, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('The Edge Between Day And Night')
    clock = pygame.time.Clock()
    time_on = False
    ticks = 0
    speed = 10
    for i in range(1, 4):
        LevelBtn(i, level_menu_group)
    current_window = StartMenu(width, height, screen)
    current_window.render()
    SoundButton(main_menu_group, level_menu_group)
    start_btn = StartButton(main_menu_group)
    current_group = main_menu_group
    running = True
    while running:
        current_group.draw(screen)
        current_group.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                coords = event.pos
                if start_btn.update(event):
                    current_window = LevelMenu(width, height, screen)
                    current_window.render()
                    current_group = level_menu_group
                current_group.update(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or \
                    event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                pass
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                current_window.change_color()
                current_group.update(event)
                current_window.render()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                pass
        status = status_dict[type(current_window)]
        pygame.display.flip()
        clock.tick(100)
        ticks += 1
    pygame.quit()
