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
        self.font_titles = pygame.font.Font('data/fonts/PixelCode-Bold.ttf', 33)
        self.font_regular = pygame.font.Font('data/fonts/PixelCode-DemiBold.ttf', 22)

    def update(self):
        pass


class StartButton(Button):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.Surface([220, 43])
        self.draw()
        self.rect = self.image.get_rect()
        self.rect.x = 330
        self.rect.y = 200

    def draw(self):
        self.text = self.font_titles.render('Start Game', True, self.font_color, self.layour_color)
        self.image.blit(self.text, self.text.get_rect())

    def update(self, *args, **kwargs):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            return True
        if args and args[0].type == pygame.KEYDOWN and event.key == pygame.K_e:
            self.layour_color, self.font_color = self.font_color, self.layour_color
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
        for i in range(3):
            self.screen.blit(self.font_titles.render(f'Level {i + 1}', True, self.font_color),
                             (50 + 330 * i, 130))
        pygame.display.update()


class Level:
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen
        self.layour_color = 'black'
        self.font_color = 'white'
        self.font = pygame.font.Font(None, 40)
        self.current_checkpoint = 0


class LevelRed(Level):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)


class LevelGreen(Level):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)


class LevelBlue(Level):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)


status_dict = {StartMenu: 'main_menu',
               LevelMenu: 'level_menu',
               LevelRed: 'red',
               LevelGreen: 'green',
               LevelBlue: 'blue'}

all_sprites = pygame.sprite.Group()
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
    current_window = StartMenu(width, height, screen)
    current_window.render()
    SoundButton(all_sprites)
    start_btn = StartButton(all_sprites)
    running = True
    while running:
        all_sprites.draw(screen)
        all_sprites.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                coords = event.pos
                if start_btn.update(event):
                    current_window = LevelMenu(width, height, screen)
                    current_window.render()
                all_sprites.update(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or \
                    event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                pass
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                current_window.change_color()
                all_sprites.update(event)
                current_window.render()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                pass
        status = status_dict[type(current_window)]
        pygame.display.flip()
        clock.tick(100)
        ticks += 1
    pygame.quit()
