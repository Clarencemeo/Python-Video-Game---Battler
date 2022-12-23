import msvcrt
import BattlePrep.inventorySlot
from BattlePrep.inventorySlot import *
from initializations import skillsEquipment
from initializations import globalVariables
import Fighters.battle
from Fighters.battle import *
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
        # rectangle for cursor is 15 by 15 in height and width
        self.cursor_rect = pygame.Rect(0, 0, 15, 15)
        self.offset = - 60  # want our cursor to be left of the menu
        self.forestMenu = pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'mainMenu.jpg')), (self.game.WIDTH, self.game.HEIGHT))

    # so the self.cursor_rect.x and self.cursor_rect.y are the positions where we want to draw the cursor.
    # The number 30 is the size of the actual cursor.
    def draw_cursor(self):
        self.game.draw_text('>', 30, self.cursor_rect.x,
                            self.cursor_rect.y, self.game.BLACK)

    # draw the cursor star for the inventory
    def draw_cursor_star(self):
        self.game.draw_text('*', 30, self.cursor_rect.x,
                            self.cursor_rect.y, self.game.WHITE)

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
                # self.game.playing = True
                self.game.curr_menu = self.game.battle
            elif self.state == "Options":
                # self.game.curr_menu = self.game.options
                self.game.curr_menu = self.game.inventory
            elif self.state == "Credits":
                self.game.curr_menu = self.game.credits
            self.run_display = False  # tell the display_menu function to stop showing the main menu


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
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
                'Made by Clarence Ortega', 15, self.game.WIDTH/2, self.game.HEIGHT/2 + 10, self.game.WHITE)
            self.blit_screen(self.game.display)


class keyboardDisable():

    def start(self):
        self.on = True

    def stop(self):
        self.on = False

    def __call__(self):
        while self.on:
            msvcrt.getwch()

    def __init__(self):
        self.on = False


class BattleMenu(Menu):  # might need to pass in parameter to indicate difficulty of enemies
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Attack"
        self.state2 = "Enemy1"
        self.skillState = 0
        self.player_turn = True
        self.attackx, self.attacky = self.mid_w, self.mid_h + 50
        self.skillsx, self.skillsy = self.mid_w, self.mid_h + 100
        self.cursor_rect.midtop = (self.attackx + self.offset, self.attacky)
        self.show_skills = False
        self.cursor_on_enemies = False
        self.cursor_on_skillMenu = False
        self.use_skill = False
        self.battleTroop = []
        # damageInfo and skillInfo record how much damage and which skill you used
        self.damageInfo = ""
        self.skillInfo = ""
        self.enemy1Info = ""
        self.enemy2Info = ""

    def display_menu(self):
        self.run_display = True
        self.battleTroop = assembleBattleTroop(globalVariables.monsterList1, 2)
        while self.run_display:
            self.display_again()

    def display_again(self):
        self.game.check_events()
        self.check_input()
        self.game.display.blit(self.forestMenu, (0, 0))
        # only draw below if not picking skills
        self.game.draw_text("Your Health: " + str(globalVariables.protagonist.getCurrHealth()), 40, self.mid_w,
                            self.mid_h-200, self.game.BLACK)
        self.game.draw_text("Your Energy: " + str(globalVariables.protagonist.getCurrEnergy()), 40, self.mid_w,
                            self.mid_h-150, self.game.BLACK)
        if self.show_skills == False:
            self.game.draw_text("Attack", 40, self.attackx,
                                self.attacky, self.game.BLACK)
            self.game.draw_text("Skills", 40, self.skillsx,
                                self.skillsy, self.game.BLACK)
        else:
            incrementer = 0
            for each_skill in globalVariables.equippedSkills:
                self.game.draw_text(each_skill.getName(), 40, self.mid_w-220+incrementer,
                                    self.mid_h+60, each_skill.getColor())
                incrementer += 170
        if (len(self.battleTroop) == 1):
            self.draw_enemy(self.battleTroop[0], 180)
        elif (len(self.battleTroop) == 2):
            self.draw_enemy(self.battleTroop[0], 180)
            self.draw_enemy(self.battleTroop[1], 0)
        self.game.draw_text(
            self.damageInfo, 30, self.mid_w, self.mid_h+150, self.game.WHITE)
        self.game.draw_text(
            self.enemy1Info, 30, self.mid_w, self.mid_h+180, self.game.RED)
        self.game.draw_text(
            self.enemy2Info, 30, self.mid_w, self.mid_h+210, self.game.RED2)
        self.draw_cursor()
        self.blit_screen(self.game.display)

    def draw_enemy(self, enemy, xOffset):
        self.game.draw_text(
            enemy.getName(), 40, self.mid_w-xOffset, self.mid_h-70, self.game.BLACK)
        self.game.draw_text(
            "Health: " + enemy.getStringHealth(), 30, self.mid_w-xOffset, self.mid_h-30, self.game.BLACK)

    def use_attack(self, skill, enemy):
        # returns True if the attack defeats an enemy
        result = skill.executeSkill(
            enemy, globalVariables.protagonist)
        self.damageInfo = result
        print(self.battleTroop)
        if (enemy.getHealth() <= 0):
            self.battleTroop.remove(enemy)
            self.damageInfo = "You defeated the " + enemy.getName() + "!"
            self.enemy1Info = ""
            self.enemy2Info = ""
            return True

    def reinitialize(self):
        self.state = "Attack"
        self.state2 = "Enemy1"
        self.cursor_on_enemies = False
        self.show_skills = False
        self.use_skill = False

    def cursor_two_options(self, tracker, state1String, state2String, x1, x2, y1, y2):
        if tracker == state1String:
            tracker = state2String
            self.cursor_rect.midtop = (x2, y2)
        elif tracker == state2String:
            tracker = state1String
            self.cursor_rect.midtop = (x1, y1)
        return tracker

    def attack(self, skill):
        position_of_enemy1X = self.mid_w-180 + self.offset
        position_of_enemy1Y = self.mid_h-70
        if len(self.battleTroop) == 1:
            if self.game.START_KEY:
                menuConfirmSound.play()
                self.use_attack(skill, self.battleTroop[0])
                self.player_turn = False
                if (len(self.battleTroop) == 1):
                    self.enemy1Info = Fighters.battle.enemyAction(
                        self.battleTroop[0])
                self.player_turn = True
            elif self.game.BACK_KEY:
                menuBackSound.play()
                self.cursor_rect.midtop = (
                    self.attackx + self.offset, self.attacky)
                self.reinitialize()
        elif len(self.battleTroop) == 2:
            if self.game.RIGHT_KEY or self.game.LEFT_KEY:
                print("zero1")
                menuHoverSound.play()
                self.state2 = self.cursor_two_options(
                    self.state2, "Enemy1", "Enemy2", position_of_enemy1X, self.mid_w + self.offset, position_of_enemy1Y, self.mid_h-70)
            elif self.game.START_KEY:
                print("oxford")
                menuConfirmSound.play()
                if self.state2 == "Enemy1":
                    self.use_attack(skill, self.battleTroop[0])
                elif self.state2 == "Enemy2":
                    if self.use_attack(skill, self.battleTroop[1]) == True:
                        self.state2 = "Enemy1"
                        self.cursor_rect.midtop = (
                            position_of_enemy1X, position_of_enemy1Y)
                self.player_turn = False
                self.enemy1Info = Fighters.battle.enemyAction(
                    self.battleTroop[0])
                if (len(self.battleTroop) > 1):
                    self.enemy2Info = Fighters.battle.enemyAction(
                        self.battleTroop[1])
                self.player_turn = True
            elif self.game.BACK_KEY:
                menuBackSound.play()
                self.state2 = "Enemy1"
                self.cursor_rect.midtop = (
                    self.attackx + self.offset, self.attacky)
                self.reinitialize()
        #self.use_skill = False

    def check_input(self):
        # this is when the player uses regular attack
        if self.cursor_on_enemies and self.player_turn:
            self.attack(globalVariables.everySkill[0])
        # this is to manage the cursor when the skill menu is open.
        elif self.use_skill and self.player_turn:
            self.attack(globalVariables.equippedSkills[self.skillState])
        elif self.show_skills and self.player_turn:
            if self.game.RIGHT_KEY:
                menuHoverSound.play()
                if self.skillState == 0:
                    self.skillState = self.cursor_two_options(self.skillState, 0, 1,
                                                              self.mid_w-220+self.offset, self.mid_w-50+self.offset, self.mid_h+60, self.mid_h+60)
                elif self.skillState == 1:
                    self.skillState = self.cursor_two_options(self.skillState, 1, 2,
                                                              self.mid_w-50+self.offset, self.mid_w+120+self.offset, self.mid_h+60, self.mid_h+60)
                elif self.skillState == 2:
                    self.skillState = self.cursor_two_options(self.skillState, 2, 3,
                                                              self.mid_w+120+self.offset, self.mid_w+290+self.offset, self.mid_h+60, self.mid_h+60)
                elif self.skillState == 3:
                    self.skillState = self.cursor_two_options(self.skillState, 3, 0,
                                                              self.mid_w+290+self.offset, self.mid_w-220+self.offset, self.mid_h+60, self.mid_h+60)
            if self.game.LEFT_KEY:
                menuHoverSound.play()
                if self.skillState == 0:
                    self.skillState = self.cursor_two_options(self.skillState, 0, 3,
                                                              self.mid_w-220+self.offset, self.mid_w+290+self.offset, self.mid_h+60, self.mid_h+60)
                elif self.skillState == 1:
                    self.skillState = self.cursor_two_options(self.skillState, 1, 0,
                                                              self.mid_w-50+self.offset, self.mid_w-220+self.offset, self.mid_h+60, self.mid_h+60)
                elif self.skillState == 2:
                    self.skillState = self.cursor_two_options(self.skillState, 2, 1,
                                                              self.mid_w+120+self.offset, self.mid_w-50+self.offset, self.mid_h+60, self.mid_h+60)
                elif self.skillState == 3:
                    self.skillState = self.cursor_two_options(self.skillState, 3, 2,
                                                              self.mid_w+290+self.offset, self.mid_w+120+self.offset, self.mid_h+60, self.mid_h+60)
            if self.game.BACK_KEY:
                menuBackSound.play()
                self.skillState = 0
                self.state = 'Attack'
                self.cursor_rect.midtop = (
                    self.attackx + self.offset, self.attacky)
                self.show_skills = False
            if self.game.START_KEY:
                #self.show_skills = False
                # self.attack(globalVariables.equippedSkills[self.skillState])
                self.cursor_rect.midtop = (
                    self.mid_w-180 + self.offset, self.mid_h-70)
                self.use_skill = True
        elif self.game.BACK_KEY:
            menuBackSound.play()
            self.cursor_rect.midtop = (
                self.attackx + self.offset, self.attacky)
            self.state == 'Attack'
            self.show_skills = False
            #self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            menuHoverSound.play()
            if self.state == 'Attack':
                self.state = "Skills"
                self.cursor_rect.midtop = (
                    self.skillsx + self.offset, self.skillsy)
            elif self.state == "Skills":
                self.state = 'Attack'
                self.cursor_rect.midtop = (
                    self.attackx + self.offset, self.attacky)
        elif self.game.START_KEY:
            menuConfirmSound.play()
            if self.state == "Attack":
                self.cursor_rect.midtop = (
                    self.mid_w-180 + self.offset, self.mid_h-70)
                self.cursor_on_enemies = True
            if self.state == 'Skills':
                self.cursor_rect.midtop = (
                    self.mid_w-220 + self.offset, self.mid_h+60)
                self.show_skills = True
                # check if the state is attack or skills and take to appropriate menu
                # maybe instead of a new menu, we can just rewrite the text?
                # because we want most of the text to stay
            pass


class InventoryMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.invMenu = pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'inventoryGrid.png')), (self.game.WIDTH, self.game.HEIGHT))
        self.cursor_rect.midtop = (60, 20)
        # these next two variables indicate how much we want to move the cursor when going horizontal or vertical.
        self.moveCursorHorizontal = 100
        self.moveCursorVertical = 130
        # The inventory system is a grid, 9x4.
        # Our bag class organizes items in a one dimensional array of 36 items (this is in the variable called "slots").
        # Our inventory grid is just a 2d array representation of the items in our bag; so 36 items represented in a 9x4 grid.
        # We will use the gridPosition to see what square in the grid we are in,
        # and then we will use that to see how it corresponds with the item in that bag slot.
        self.gridPosition = 1

    def display_menu(self):
        self.run_display = True
        globalVariables.itemBag.addToInventory(skillsEquipment.silverSword)
        globalVariables.itemBag.addToInventory(skillsEquipment.silverSword)
        print(globalVariables.itemBag.slots)
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            # obviously this isn't going to be in the final iteration!
            # render is responsible for drawing each item in each inventorySlot in the bag
            globalVariables.itemBag.render(self.game.display)
            # self.game.display.blit(self.invMenu, (0, 0))

            # should loop through Inventory and access each InventorySlot
            self.draw_cursor_star()
            self.blit_screen(self.game.display)

    def calc_pos_x(self):
        # so... each square in the grid is 100x100.
        # within each square, we want the cursor to be 60 units in.

        # go to the square before (self.gridposition-1), mul
        initialResult = ((self.gridPosition-1) * 100) + 60
        while initialResult > 900:
            initialResult -= 900
        return initialResult

    def calc_pos_y(self):
        initialResult = ((self.gridPosition-9) * 100) + 20
        while initialResult > 400:
            initialResult -= 400
        return initialResult

    def move_cursor(self):
        # Thinking question: How do we know which slot in the grid the cursor is in?
        # ANSWER:
        # Start at position 1. Everytime you move right, increment position by 1, and decrement by 1 when going left.
        # When you go down, you are actually just moving your position up by 9, and vice versa when going up.
        if self.game.BACK_KEY:
            menuBackSound.play()
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.START_KEY:
            # how are we going to switch between screens based on the slot?
            # maybe it will always switch to the same menu, but the menu changes based on the item selected!
            # this if statement checks if the inventorySlot we are hovering actually has an item
            if isinstance(globalVariables.itemBag.slots[self.gridPosition], BattlePrep.inventorySlot.InventorySlot):
                print("success")
            # correspond the grid position with the index in slots!!!
            menuHoverSound.play()
        elif self.game.RIGHT_KEY:
            menuHoverSound.play()
            if self.gridPosition == 36:
                pass
            elif self.gridPosition % 9 == 0:
                self.gridPosition += 1
                self.cursor_rect.midtop = (
                    self.calc_pos_x(), self.calc_pos_y())
            else:
                self.gridPosition += 1
                self.cursor_rect.midtop = (
                    self.calc_pos_x(), self.cursor_rect.y)

        elif self.game.LEFT_KEY:
            menuHoverSound.play()
            if self.gridPosition == 1:
                pass
            elif self.gridPosition % 9 == 1:
                self.gridPosition -= 1
                self.cursor_rect.midtop = (
                    self.calc_pos_x(), self.calc_pos_y())
            else:
                self.gridPosition -= 1
                self.cursor_rect.midtop = (
                    self.calc_pos_x(), self.cursor_rect.y)

    def check_input(self):
        self.move_cursor()


"""
        elif self.game.UP_KEY:
            menuHoverSound.play()
            self.gridPosition -= 9
            self.cursor_rect.midtop = (
                self.cursor_rect.x, self.calc_pos_y())

        elif self.game.DOWN_KEY:
            menuHoverSound.play()
            self.gridPosition += 9
            self.cursor_rect.midtop = (
                self.cursor_rect.x, self.calc_pos_y())
    # use ifInstance when clicking enter... if you click enter on something that has no class, then do nothing!
"""
