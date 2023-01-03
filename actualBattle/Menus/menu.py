from initializations.skillsEquipment import *
import pygame
import os
import random
import copy
pygame.mixer.init()
global protagonist
protagonist = ""

skills = Skills()
enemies = Enemies()
equips = Equips()
classes = Classes()


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.WIDTH/2, self.game.HEIGHT/2
        self.run_display = True
        self.skills = skills
        self.enemies = enemies
        self.equips = equips
        self.classes = classes
        self.menuConfirmSound = pygame.mixer.Sound(
            os.path.join('Assets/menuSelect.wav'))
        self.menuHoverSound = pygame.mixer.Sound(
            os.path.join('Assets/menuHover.wav'))
        self.menuBackSound = pygame.mixer.Sound(
            os.path.join('Assets/menuBack.wav'))
        self.menuErrorSound = pygame.mixer.Sound(
            os.path.join('Assets/menu_error.wav'))
        #self.protag = globalVariables.protagonist
        self.protag = protagonist
        #self.monsters = globalVariables.monsterList1
        self.monsters = {
            "Slime": self.enemies.slimeEnemy, "Bat": self.enemies.batEnemy, "Ghost": self.enemies.ghostEnemy, "Spider": self.enemies.spiderEnemy, "Unicorn": self.enemies.unicornEnemy, "Wolf": self.enemies.wolfEnemy, "Skeleton": self.enemies.skeletonEnemy}
        # rectangle for cursor is 15 by 15 in height and width
        self.cursor_rect = pygame.Rect(0, 0, 15, 15)
        self.offset = - 65  # want our cursor to be left of the menu
        self.backMenu = pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'mainMenu.jpg')), (self.game.WIDTH, self.game.HEIGHT))

    # so the self.cursor_rect.x and self.cursor_rect.y are the positions where we want to draw the cursor.
    # The number 30 is the size of the actual cursor.
    def draw_cursor(self):
        self.game.draw_text('>', 50, self.cursor_rect.x,
                            self.cursor_rect.y, self.game.BLACK)

    # draw the cursor star for the inventory
    def draw_cursor_star(self):
        self.game.draw_text('*', 30, self.cursor_rect.x,
                            self.cursor_rect.y, self.game.WHITE)

    def blit_screen(self, display):
        self.game.window.blit(display, ((0, 0)))
        pygame.display.update()
        self.game.reset_keys()

    def cursor_two_options(self, cursor, tracker, state1String, state2String, x1, x2, y1, y2):
        if tracker == state1String:
            tracker = state2String
            self.cursor_rect.midtop = (x2, y2)
        elif tracker == state2String:
            tracker = state1String
            self.cursor_rect.midtop = (x1, y1)
        return tracker

    def cursor_mult_options(self, tracker, x, y, xAdjustment, yAdjustment, capacity, reverse):
        tempClassState = tracker
        print(tracker)
        if tracker >= capacity-1 and not reverse:
            tracker = self.cursor_two_options(
                self.cursor_rect, tracker, tracker, 0, x+(tempClassState*xAdjustment), x+((0)*xAdjustment), y+(tempClassState*yAdjustment), y+((0)*yAdjustment))
        elif tracker == 0 and reverse:
            tracker = self.cursor_two_options(
                self.cursor_rect, tracker, 0, capacity-1, x+(tempClassState*xAdjustment), x+((capacity-1)*xAdjustment), y+(tempClassState*yAdjustment), y+((capacity-1)*yAdjustment))
        elif not reverse:
            tracker = self.cursor_two_options(
                self.cursor_rect, tracker, tracker, tracker+1, x+(tempClassState*xAdjustment), x+((tempClassState+1)*xAdjustment), y+(tempClassState*yAdjustment), y+((tempClassState+1)*yAdjustment))
        elif reverse:
            tracker = self.cursor_two_options(
                self.cursor_rect, tracker, tracker, tracker-1, x+(tempClassState*xAdjustment), x+((tempClassState-1)*xAdjustment), y+(tempClassState*yAdjustment), y+((tempClassState-1)*yAdjustment))
        return tracker

    def draw_info(self):
        self.game.draw_text("Health: " + str(self.protag.currHealth), 50, self.mid_w,
                            self.mid_h-370, self.game.BLACK)
        self.game.draw_text("Mana: " + str(self.protag.currEnergy), 50, self.mid_w,
                            self.mid_h-270, self.game.BLACK)
        self.game.draw_text("Level: " + str(self.protag.level), 50, self.mid_w,
                            self.mid_h-170, self.game.BLACK)
        if self.protag.getState()[0] != "":
            self.game.draw_text("Ailments: " + self.protag.getState()[0], 50, self.mid_w,
                                self.mid_h-70, (229, 255, 0))

    def deepCopyEnemy(self, enemy):
        return copy.deepcopy(self.monsters[enemy])
