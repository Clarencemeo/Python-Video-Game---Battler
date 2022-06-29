import pygame
import os
pygame.mixer.init()
menuConfirmSound = pygame.mixer.Sound(os.path.join('Assets/menuSelect.wav'))
menuHoverSound = pygame.mixer.Sound(os.path.join('Assets/menuHover.wav'))
menuBackSound = pygame.mixer.Sound(os.path.join('Assets/menuBack.wav'))


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.WIDTH/2, self.game.HEIGHT/2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 15, 15)
        self.offset = - 60  # want our cursor to be left of the menu

    def draw_cursor(self):
        self.game.draw_text('>', 30, self.cursor_rect.x,
                            self.cursor_rect.y, self.game.BLACK)

    def blit_screen(self, display):
        self.game.window.blit(display, ((0, 0)))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):  # inherit values of base class menu
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"  # each option
        # get x and y pos of each text option
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.forestMenu = pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'mainMenu.jpg')), (self.game.WIDTH, self.game.HEIGHT))

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.forestMenu, (0, 0))
            self.game.draw_text(
                'Turn Based Dungeon', 50, self.game.WIDTH/2, self.game.HEIGHT/2 - 20, self.game.BLACK)
            self.game.draw_text("Start Game", 20, self.startx,
                                self.starty, self.game.BLACK)
            self.game.draw_text("Options", 20, self.optionsx,
                                self.optionsy, self.game.BLACK)
            self.game.draw_text("Credits", 20, self.creditsx,
                                self.creditsy, self.game.BLACK)
            self.draw_cursor()
            self.blit_screen(self.game.display)

    def move_cursor(self):
        # tracks where the cursor should be
        if self.game.DOWN_KEY:
            menuHoverSound.play()
            if self.state == "Start":
                self.cursor_rect.midtop = (
                    self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == "Options":
                self.cursor_rect.midtop = (
                    self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == "Credits":
                self.cursor_rect.midtop = (
                    self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            menuHoverSound.play()
            if self.state == "Start":
                self.cursor_rect.midtop = (
                    self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == "Options":
                self.cursor_rect.midtop = (
                    self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == "Credits":
                self.cursor_rect.midtop = (
                    self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:  # when player clicks enter
            menuConfirmSound.play()
            if self.state == "Start":
                self.game.playing = True
            elif self.state == "Options":
                self.game.curr_menu = self.game.options
            elif self.state == "Credits":
                self.game.curr_menu = self.game.credits
            self.run_display = False  # tell the display_menu function to stop showing the main menu


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):  # should be same name as one above
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text(
                "Options", 20, self.game.WIDTH/2, self.game.HEIGHT/2 - 30, self.game.WHITE)
            self.game.draw_text('Volume', 15, self.volx,
                                self.voly, self.game.WHITE)
            self.game.draw_text("Controls", 15, self.controlsx,
                                self.controlsy, self.game.WHITE)
            self.draw_cursor()
            self.blit_screen(self.game.display)

    def check_input(self):
        if self.game.BACK_KEY:
            menuBackSound.play()
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            menuHoverSound.play()
            if self.state == 'Volume':
                self.state = "Controls"
                self.cursor_rect.midtop = (
                    self.controlsx + self.offset, self.controlsy)
            elif self.state == "Controls":
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            menuConfirmSound.play()
            pass  # take them to the volume menu


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.BACK_KEY:
                menuBackSound.play()
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text(
                'Credits', 20, self.game.WIDTH/2, self.game.HEIGHT/2 - 20, self.game.WHITE)
            self.game.draw_text(
                'Made by Clarence', 15, self.game.WIDTH/2, self.game.HEIGHT/2 + 10, self.game.WHITE)
            self.blit_screen(self.game.display)
