import pygame


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


class Start_menu(Window):

    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)

    def render(self):

        self.title = self.font_titles.render('The Edge Between Day And Night', True, self.font_color)
        self.start_button = self.font_titles.render('Start', True, self.font_color)
        self.music_disc = pygame.image.load("data/images/music_disc.png")
        ## TODO сделать запрос на трек
        self.music_label = self.font_regular.render('Track_Title - Author', True, self.font_color)
        self.screen.fill(self.layour_color)
        self.screen.blit(self.title,
                         (self.width / 2 - self.title.get_width() / 2, 20))
        self.screen.blit(self.start_button,
                         (self.width / 2 - self.start_button.get_width() / 2,
                          150))
        self.screen.blit(self.music_disc, (10, 350))
        self.screen.blit(self.music_label, (70, 356))
        pygame.display.update()


class Level_menu(Window):
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


class Level_red(Level):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)


class Level_green(Level):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)


class Level_blue(Level):
    def __init__(self, width, height, screen):
        super().__init__(width, height, screen)


status_dict = {Start_menu: 'main_menu',
               Level_menu: 'level_menu',
               Level_red: 'red',
               Level_green: 'green',
               Level_blue: 'blue'}

status = 'main_menu'
if __name__ == '__main__':
    pygame.init()
    size = width, height = 900, 400
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('The Edge Between Day And Night')
    clock = pygame.time.Clock()
    time_on = False
    ticks = 0
    speed = 10
    current_window = Start_menu(width, height, screen)
    current_window.render()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and status == 'main_menu':
                coords = event.pos
                if coords[0] in range(345, 470) and coords[1] in range(130, 190):
                    current_window = Level_menu(width, height, screen)
                    current_window.render()
                else:
                    print(coords)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or \
                    event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                pass
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                current_window.change_color()
                current_window.render()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                pass
        status = status_dict[type(current_window)]
        pygame.display.flip()
        clock.tick(100)
        ticks += 1
    pygame.quit()
