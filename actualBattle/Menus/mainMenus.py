from . import menu
from . import setupMenus


class MainMenu(menu.Menu):  # inherit values of base class menu
    def __init__(self, game):
        menu.Menu.__init__(self, game)
        self.state = "Start"  # each option
        # get x and y pos of each text option
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.backMenu, (0, 0))
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
            self.menuHoverSound.play()
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
            self.menuHoverSound.play()
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
            self.menuConfirmSound.play()
            if self.state == "Start":
                # self.game.playing = True
                # self.battle = BattleMenu(self.game)
                # self.game.curr_menu = self.battle
                self.game.curr_menu = setupMenus.classMenu(self.game)
            elif self.state == "Options":
                # self.game.curr_menu = self.game.options
                # self.game.curr_menu = self.game.inventory
                pass
            elif self.state == "Credits":
                self.game.curr_menu = self.game.credits
            self.run_display = False  # tell the display_menu function to stop showing the main menu


class OptionsMenu(menu.Menu):
    def __init__(self, game):
        menu.Menu.__init__(self, game)
        self.state = 'Volume'
        # draw the volume and controls text 20 and 40 units away from the midpoints, respectively.
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        # the top middle position of the cursor is going to be at the height of the volume text,
        # and the horizontal position is going to be at the same as the volume text, except there is a -60 offset.
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):  # should be same name as one above
        self.run_display = True
        while self.run_display:
            # send a signal if an event is used
            self.game.check_events()
            # receive the signal from the above line and then move cursor based on that signal
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
            self.menuBackSound.play()
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            self.menuHoverSound.play()
            if self.state == 'Volume':
                self.state = "Controls"
                self.cursor_rect.midtop = (
                    self.controlsx + self.offset, self.controlsy)
            elif self.state == "Controls":
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            self.menuConfirmSound.play()
            pass  # take them to the volume menu


class CreditsMenu(menu.Menu):
    def __init__(self, game):
        menu.Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.BACK_KEY:
                self.menuBackSound.play()
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text(
                'Credits', 20, self.game.WIDTH/2, self.game.HEIGHT/2 - 20, self.game.WHITE)
            self.game.draw_text(
                'Made by Clarence Ortega', 15, self.game.WIDTH/2, self.game.HEIGHT/2 + 10, self.game.WHITE)
            self.blit_screen(self.game.display)
