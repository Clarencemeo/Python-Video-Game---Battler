import pygame
from menu import *
pygame.font.init()


class mainGame():
    def __init__(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.RIGHT_KEY, self.LEFT_KEY = False, False, False, False, False, False
        self.WIDTH, self.HEIGHT = 900, 500
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (73, 122, 7)
        self.RED = (245, 40, 29)
        self.RED2 = (204, 18, 8)
        # self.running refers to when the game is open, self.playing refers to when the player is actually playing the game (i.e not in main menu)
        self.running, self.playing = True, False
        # blitzing the display onto the window
        self.display = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Turn Based")
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.inventory = InventoryMenu(self)
        self.credits = CreditsMenu(self)
        self.battle = BattleMenu(self)
        self.curr_menu = self.main_menu

    # Runs different things based on which event is detected; events include closing the game and pressing down certain buttons
    # will send a signal based on which event is triggered; these signals incluide self.START_KEY, etc.
    # If the event is QUIT, then the game will not send a signal; it will simply quit.
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False  # stop whatever menu is currently running
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True

    def game_loop(self):
        # self.playing is only true when you click start on the MainMenu class
        while self.playing:
            self.check_events()
            if self.START_KEY:
                # ensures that it doesn't loop again
                self.playing = False
            # NEXT STEPS: SHOULD SWITCH TO A NEW MENU
            self.curr_menu = self.battle
            pygame.display.update()
            self.reset_keys()

    def reset_keys(self):
        # if we don't reset the keys, then it will interpret the keys as always being pressed down
        # after the first time they are pressed down.
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.RIGHT_KEY, self.LEFT_KEY = False, False, False, False, False, False

    def draw_text(self, text, size, x, y, color):
        font = pygame.font.SysFont('arial', size)
        text_surface = font.render(text, 1, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
