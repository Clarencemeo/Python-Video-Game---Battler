from . import menu
from . import setupMenus


class MainMenu(menu.Menu):  # inherit values of base class menu
    def __init__(self, game):
        menu.Menu.__init__(self, game)
        self.state = "Start"  # each option
        # get x and y pos of each text option
        self.startx, self.starty = self.mid_w, self.mid_h + 60
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 120
        self.cursor_rect.midtop = (self.startx + self.offset - 50, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.backMenu, (0, 0))
            self.game.draw_text(
                'Turn Based Dungeon', 50, self.game.WIDTH/2, self.game.HEIGHT/2 - 20, self.game.BLACK)
            self.game.draw_text("Start Game", 40, self.startx,
                                self.starty, self.game.BLACK)
            self.game.draw_text("Credits", 40, self.creditsx,
                                self.creditsy, self.game.BLACK)
            self.draw_cursor()
            self.blit_screen(self.game.display)

    def move_cursor(self):
        # tracks where the cursor should be
        if self.game.DOWN_KEY or self.game.UP_KEY:
            self.menuHoverSound.play()
            self.state = self.cursor_two_options(self.cursor_rect, self.state, "Start", "Credits", self.startx +
                                                 self.offset - 50, self.creditsx + self.offset - 50, self.starty, self.creditsy)

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:  # when player clicks enter
            self.menuConfirmSound.play()
            if self.state == "Start":
                # self.game.playing = True
                # self.battle = BattleMenu(self.game)
                # self.game.curr_menu = self.battle
                self.game.curr_menu = setupMenus.classMenu(self.game)
            elif self.state == "Credits":
                self.game.curr_menu = CreditsMenu(self.game)
            self.run_display = False  # tell the display_menu function to stop showing the main menu


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
