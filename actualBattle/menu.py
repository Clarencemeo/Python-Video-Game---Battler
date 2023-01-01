import msvcrt
import BattlePrep.inventorySlot
from BattlePrep.inventorySlot import *
from initializations import skillsEquipment
from initializations import globalVariables
import Fighters.battle
from Fighters.battle import *
from Fighters.enemy import Enemy
import pygame
import os
pygame.mixer.init()
menuConfirmSound = pygame.mixer.Sound(os.path.join('Assets/menuSelect.wav'))
menuHoverSound = pygame.mixer.Sound(os.path.join('Assets/menuHover.wav'))
menuBackSound = pygame.mixer.Sound(os.path.join('Assets/menuBack.wav'))
menuErrorSound = pygame.mixer.Sound(os.path.join('Assets/menu_error.wav'))
victorySound = pygame.mixer.Sound(os.path.join('Assets/battleVictory.wav'))


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.WIDTH/2, self.game.HEIGHT/2
        self.run_display = True
        self.protag = globalVariables.protagonist
        # rectangle for cursor is 15 by 15 in height and width
        self.cursor_rect = pygame.Rect(0, 0, 15, 15)
        self.offset = - 65  # want our cursor to be left of the menu
        self.forestMenu = pygame.transform.scale(pygame.image.load(
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
                self.battle = BattleMenu(self.game)
                self.game.curr_menu = self.battle
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


class LevelUpMenu(Menu):
    def __init__(self, game, expGained):
        Menu.__init__(self, game)
        self.expGained = expGained
        self.statState = 0
        self.statInfo = ""
        self.triggerKey = False
        self.tempStat = 0

    def displayStatInfo(self):
        if self.statState == 0:
            self.statInfo = "Strength increases damage dealt with physical attacks and skills."
        if self.statState == 1:
            self.statInfo = "Magic increases damage dealt with magical attacks and skills."
        if self.statState == 2:
            self.statInfo = "Defense reduces damage received from physical attacks and skills."
        if self.statState == 3:
            self.statInfo = "MagDef reduces damage received from magical attacks and skills."
        if self.statState == 4:
            self.statInfo = "Speed determines the turn order of battles."
        if self.statState == 5:
            self.statInfo = "Luck determines chance of criticals and running into lucky scenarios."
        if self.statState == 6:
            self.statInfo = "Will you confirm this option?"

    def display_menu(self):
        self.run_display = True
        self.cursor_rect.midtop = (
            self.mid_w-550 + self.offset-50, self.mid_h-250)
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.forestMenu, (0, 0))
            self.displayStatInfo()
            self.game.draw_text("LEVEL UP!", 60, self.mid_w,
                                self.mid_h-450, self.game.WHITE)
            self.game.draw_text("You earned " + str(self.expGained) + " EXP and leveled up to level " + str(globalVariables.protagonist.getLevel()) + "! Choose which stats to level.", 40, self.mid_w,
                                self.mid_h-370, self.game.BLACK)
            self.game.draw_text("Strength: " + str(self.protag.getAttackDamage()), 40, self.mid_w-550,
                                self.mid_h-250, self.game.WHITE)
            self.game.draw_text("Magic: " + str(self.protag.getMagicDamage()), 40, self.mid_w-550,
                                self.mid_h-180, self.game.WHITE)
            self.game.draw_text("Defense: " + str(self.protag.getPhysicalDefense()), 40, self.mid_w-550,
                                self.mid_h-110, self.game.WHITE)
            self.game.draw_text("MagDef: " + str(self.protag.getMagicalDefense()), 40, self.mid_w-550,
                                self.mid_h-40, self.game.WHITE)
            self.game.draw_text("Speed: " + str(self.protag.getSpeed()), 40, self.mid_w-550,
                                self.mid_h+30, self.game.WHITE)
            self.game.draw_text("Luck: " + str(self.protag.getLuck()), 40, self.mid_w-550,
                                self.mid_h+100, self.game.WHITE)
            self.game.draw_text(self.statInfo, 40, self.mid_w,
                                self.mid_h-320, self.game.WHITE)
            self.game.draw_text("Confirm", 60, self.mid_w,
                                self.mid_h+400, self.game.WHITE)
            self.draw_cursor()
            self.blit_screen(self.game.display)

    def confirmation(self):
        # if self.statState == 0:
        self.statState = 6  # confirm  button
        self.cursor_rect.midtop = (
            self.mid_w + self.offset-50, self.mid_h+400)
        if self.game.START_KEY:
            print("yo")
            self.victory = VictoryMenu(self.game, self.expGained)
            self.game.curr_menu = self.victory
            menuConfirmSound.play()
            self.run_display = False
        elif self.game.BACK_KEY:
            menuBackSound.play()
            self.statState = 0
            self.cursor_rect.midtop = (
                self.mid_w-550 + self.offset-50, self.mid_h-250)
            print(self.tempStat)
            if self.tempStat == 0:
                self.protag.adjustattackDamage(-1)
            elif self.tempStat == 1:
                self.protag.adjustmagicDamage(-1)
            elif self.tempStat == 2:
                self.protag.adjustDefense(-1)
            elif self.tempStat == 3:
                self.protag.adjustMagDef(-1)
            elif self.tempStat == 4:
                self.protag.adjustSpeed(-1)
            elif self.tempStat == 5:
                self.protag.adjustLuck(-1)
            self.triggerKey = False

    def check_input(self):
        cursorXpos = self.mid_w-550+self.offset-50
        if self.triggerKey:
            self.confirmation()
        elif self.game.START_KEY:
            menuConfirmSound.play()
            if self.statState == 0:
                self.protag.adjustattackDamage(1)
            elif self.statState == 1:
                self.protag.adjustmagicDamage(1)
            elif self.statState == 2:
                self.protag.adjustDefense(1)
            elif self.statState == 3:
                self.protag.adjustMagDef(1)
            elif self.statState == 4:
                self.protag.adjustSpeed(1)
            elif self.statState == 5:
                self.protag.adjustLuck(1)
            self.tempStat = self.statState
            self.triggerKey = True
        elif self.game.DOWN_KEY:
            menuHoverSound.play()
            if self.statState == 0:
                self.statState = self.cursor_two_options(
                    self.cursor_rect, self.statState, 0, 1, cursorXpos, cursorXpos, self.mid_h-250, self.mid_h-180)
            elif self.statState == 1:
                self.statState = self.cursor_two_options(
                    self.cursor_rect, self.statState, 1, 2, cursorXpos, cursorXpos, self.mid_h-180, self.mid_h-110)
            elif self.statState == 2:
                self.statState = self.cursor_two_options(
                    self.cursor_rect, self.statState, 2, 3, cursorXpos, cursorXpos, self.mid_h-110, self.mid_h-40)
            elif self.statState == 3:
                self.statState = self.cursor_two_options(
                    self.cursor_rect, self.statState, 3, 4, cursorXpos, cursorXpos, self.mid_h-40, self.mid_h+30)
            elif self.statState == 4:
                self.statState = self.cursor_two_options(
                    self.cursor_rect, self.statState, 4, 5, cursorXpos, cursorXpos, self.mid_h+30, self.mid_h+100)
        elif self.game.UP_KEY:
            menuHoverSound.play()
            if self.statState == 1:
                self.statState = self.cursor_two_options(
                    self.cursor_rect, self.statState, 1, 0, cursorXpos, cursorXpos, self.mid_h-180, self.mid_h-250)
            elif self.statState == 2:
                self.statState = self.cursor_two_options(
                    self.cursor_rect, self.statState, 2, 1, cursorXpos, cursorXpos, self.mid_h-110, self.mid_h-180)
            elif self.statState == 3:
                self.statState = self.cursor_two_options(
                    self.cursor_rect, self.statState, 3, 2, cursorXpos, cursorXpos, self.mid_h-40, self.mid_h-110)
            elif self.statState == 4:
                self.statState = self.cursor_two_options(
                    self.cursor_rect, self.statState, 4, 3, cursorXpos, cursorXpos, self.mid_h+30, self.mid_h-40)
            elif self.statState == 5:
                self.statState = self.cursor_two_options(
                    self.cursor_rect, self.statState, 5, 4, cursorXpos, cursorXpos, self.mid_h-40, self.mid_h+30)


class VictoryMenu(Menu):
    def __init__(self, game, expGained):
        Menu.__init__(self, game)
        self.expGained = expGained

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.forestMenu, (0, 0))
            self.game.draw_text("VICTORY!", 60, self.mid_w,
                                self.mid_h-450, self.game.WHITE)
            self.game.draw_text("Current Level: " + str(self.protag.getLevel()), 40, self.mid_w,
                                self.mid_h-350, self.game.BLACK)
            self.game.draw_text("EXP Earned: " + str(self.expGained), 40, self.mid_w,
                                self.mid_h-250, self.game.BLACK)
            self.game.draw_text("EXP Until Next Level: " + str(self.protag.getLevel()*25 - self.protag.getExperience()), 40, self.mid_w,
                                self.mid_h-150, self.game.BLACK)
            self.game.draw_text("Health: " + str(self.protag.getCurrHealth()) + "/" + str(self.protag.getHealth()), 40, self.mid_w,
                                self.mid_h-50, self.game.BLACK)
            self.game.draw_text("Energy: " + str(self.protag.getCurrEnergy()) + "/" + str(self.protag.getEnergy()), 40, self.mid_w,
                                self.mid_h+50, self.game.BLACK)
            self.draw_cursor()
            self.blit_screen(self.game.display)

    def check_input(self):
        pass


class gameOverMenu(Menu):
    def __init__(self, game, finishingBlow):
        Menu.__init__(self, game)
        self.finishingBlow = finishingBlow

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.forestMenu, (0, 0))
            self.game.draw_text("DEFEAT!", 60, self.mid_w,
                                self.mid_h-450, self.game.RED)
            self.game.draw_text("Moment of Death: " + self.finishingBlow, 40, self.mid_w,
                                self.mid_h-350, self.game.BLACK)
            self.game.draw_text("Current Level: " + str(self.protag.getLevel()), 40, self.mid_w,
                                self.mid_h-250, self.game.BLACK)
            self.game.draw_text("Continue?", 60, self.mid_w,
                                self.mid_h+400, self.game.WHITE)
            self.cursor_rect.midtop = (
                self.mid_w+self.offset-70, self.mid_h+400)
            self.draw_cursor()
            self.blit_screen(self.game.display)

    def check_input(self):
        if self.game.START_KEY:
            menuConfirmSound.play()
            self.restart = MainMenu(self.game)
            self.game.curr_menu = self.restart
            initializations.skillsEquipment.init()  # reset protag stats
            self.run_display = False


class BattleMenu(Menu):  # might need to pass in parameter to indicate difficulty of enemies
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Attack"
        self.state2 = "Enemy1"
        self.speedList = []
        # self.turnList will have a list of names in descending order
        # of their speed stat
        self.turnList = []
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
        self.information1 = ("", self.game.BLACK)
        self.information2 = ("", self.game.BLACK)
        self.information3 = ("", self.game.BLACK)
        self.expGained = 0
        self.defeatMessage = 0

    def levelUpCalculation(self, theProtagonist, experiencePointsGained):
        # every level requires 25 more exp than the previous
        levelCap = theProtagonist.getLevel() * 25
        theProtagonist.adjustExperience(experiencePointsGained)
        if (theProtagonist.getExperience() >= levelCap):
            # leftOverExperience after leveling up
            leftoverExperience = theProtagonist.getExperience() - levelCap
            # reset experience after leveling up
            theProtagonist.setExperience(0)
            # add over the leftover experience
            theProtagonist.adjustExperience(leftoverExperience)
            theProtagonist.adjustLevel(1)
            # actually level up
            # bottom condtional statement just in case the leftOverExperience ended up resulting in another level up.
            return True
        elif (theProtagonist.getExperience() >= theProtagonist.getLevel() * 25):
            pass
        else:
            return False

    def winBattle(self):
        if len(self.battleTroop) == 0:
            victorySound.play()
            # if level up, go to levelup menu, else go to victoryMenu
            if self.levelUpCalculation(globalVariables.protagonist, self.expGained):
                self.levelUp = LevelUpMenu(self.game, self.expGained)
                self.game.curr_menu = self.levelUp
            else:
                self.victory = VictoryMenu(self.game, self.expGained)
                self.game.curr_menu = self.victory
            self.run_display = False
            # exit()

    def display_menu(self):
        self.run_display = True
        self.battleTroop = assembleBattleTroop(globalVariables.monsterList1, 2)
        for i in self.battleTroop:
            self.expGained += i.getExperienceReward()
        while self.run_display:
            self.display_again()

    def holdeR(self):
        self.restart = MainMenu(self.game)
        self.game.curr_menu = self.restart
        initializations.skillsEquipment.init()  # reset protag stats
        self.run_display = False

    def display_again(self):
        self.game.check_events()
        self.check_input()
        self.game.display.blit(self.forestMenu, (0, 0))
        self.winBattle()
        self.turnOrder = "Turn Order: " + self.calculate_turn_order()
        self.game.draw_text("Your Health: " + str(globalVariables.protagonist.getCurrHealth()), 40, self.mid_w,
                            self.mid_h-400, self.game.BLACK)
        self.game.draw_text("Your Energy: " + str(globalVariables.protagonist.getCurrEnergy()), 40, self.mid_w,
                            self.mid_h-350, self.game.BLACK)
        if (len(self.battleTroop) == 1):
            self.draw_enemy(self.battleTroop[0], 180)
        elif (len(self.battleTroop) == 2):
            self.draw_enemy(self.battleTroop[0], 180)
            self.draw_enemy(self.battleTroop[1], 0)
        self.game.draw_text(
            self.information1[0], 30, self.mid_w, self.mid_h+150, self.information1[1])
        self.game.draw_text(
            self.information2[0], 30, self.mid_w, self.mid_h+180, self.information2[1])
        self.game.draw_text(
            self.information3[0], 30, self.mid_w, self.mid_h+210, self.information3[1])
        self.game.draw_text(self.turnOrder, 30, self.mid_w,
                            self.mid_h-290, self.game.WHITE)

        if self.show_skills == False:
            self.game.draw_text("Attack", 40, self.attackx,
                                self.attacky, self.game.BLACK)
            self.game.draw_text("Skills", 40, self.skillsx,
                                self.skillsy, self.game.BLACK)
        ###

        # occurs when user is selecting a skill
        elif self.show_skills == True:
            incrementer = 0
            for each_skill in globalVariables.equippedSkills:
                self.game.draw_text(globalVariables.equippedSkills[self.skillState].getDescription(), 40, self.mid_w,
                                    self.mid_h+10, self.game.BLACK)
                self.game.draw_text(each_skill.getName(), 40, self.mid_w-220+incrementer,
                                    self.mid_h+60, each_skill.getColor())
                self.game.draw_text("Energy: " + str(each_skill.getEnergy()), 25, self.mid_w-220+incrementer,
                                    self.mid_h+90, self.game.BLACK)
                self.game.draw_text("Type: " + each_skill.getSkillType(), 25, self.mid_w-220+incrementer,
                                    self.mid_h+120, self.game.BLACK)
                incrementer += 170
        ###
        self.draw_cursor()
        self.blit_screen(self.game.display)

    def draw_enemy(self, enemy, xOffset):
        self.game.draw_text(
            enemy.getName(), 40, self.mid_w-xOffset, self.mid_h-210, self.game.BLACK)
        self.game.draw_text(
            "Health: " + enemy.getStringHealth(), 30, self.mid_w-xOffset, self.mid_h-170, self.game.BLACK)

    def reinitialize(self):
        self.state = "Attack"
        self.state2 = "Enemy1"
        self.skillState = 0
        self.cursor_on_enemies = False
        self.show_skills = False
        self.use_skill = False

    def calculate_turn_order(self):
        self.speedDict = {}
        playerSpeed = globalVariables.protagonist.getSpeed()
        self.speedDict['Player'] = playerSpeed
        # create a dictionary that match
        # each player & enemy with their respective speeds.
        for eachEnemy in self.battleTroop:
            self.speedDict[eachEnemy.getName()] = eachEnemy.getSpeed()
        # generate a list comprised of tuples of the form
        # (Name, Speed) in descending order of speed.
        self.speedList = sorted(self.speedDict.items(),
                                key=lambda x: x[1], reverse=True)
        # turnOrder will be a list of names in descending order of speed
        turnString = ""
        self.turnList = []
        for eachTuple in self.speedList:
            self.turnList.append(eachTuple[0])
            turnString += " -> "
            turnString += (eachTuple[0])
        return turnString

    def attack(self, skill):
        position_of_enemy1X = self.mid_w-180 + self.offset
        position_of_enemy1Y = self.mid_h-210
        if (skill.getEnergy() > self.protag.getCurrEnergy()):
            menuErrorSound.play()
            self.state2 = "Enemy1"
            self.cursor_rect.midtop = (
                self.attackx + self.offset, self.attacky)
            self.reinitialize()
            return
        elif self.game.RIGHT_KEY or self.game.LEFT_KEY:
            if (len(self.battleTroop) >= 2):
                menuHoverSound.play()
                self.state2 = self.cursor_two_options(
                    self.cursor_rect, self.state2, "Enemy1", "Enemy2", position_of_enemy1X, self.mid_w + self.offset, position_of_enemy1Y, self.mid_h-210)
            else:
                pass
        elif self.game.START_KEY:
            menuConfirmSound.play()
            if self.state2 == "Enemy1":
                enemyTarget = self.battleTroop[0]
            elif self.state2 == "Enemy2":
                enemyTarget = self.battleTroop[1]
            self.player_turn = False
            self.attackTurnOrder(enemyTarget, skill)
            self.player_turn = True
        elif self.game.BACK_KEY:
            menuBackSound.play()
            self.state2 = "Enemy1"
            self.cursor_rect.midtop = (
                self.attackx + self.offset, self.attacky)
            self.reinitialize()

    def deleteFromList(self, element):
        for i in self.turnList:
            if i == element:
                self.turnList.remove(i)

    def attackTurnOrder(self, enemyTarget, skill):
        counter = 1
        for eachEntity in self.turnList:
            if eachEntity == "Player":
                skillInfo = skill.executeSkill(
                    enemyTarget, globalVariables.protagonist)
                if (enemyTarget.getHealth() <= 0):
                    self.battleTroop.remove(enemyTarget)
                    skillInfo = "You defeated the " + enemyTarget.getName() + "!"
                    self.cursor_rect.midtop = (
                        self.mid_w-180 + self.offset, self.mid_h-210)
                    self.deleteFromList(enemyTarget.getName())
                    self.state2 = "Enemy1"
                    self.information1 = ("", self.game.BLACK)
                    self.information2 = ("", self.game.BLACK)
                    self.information3 = ("", self.game.BLACK)
                if counter == 1:
                    self.information1 = (skillInfo, self.game.WHITE)
                elif counter == 2:
                    self.information2 = (skillInfo, self.game.WHITE)
                elif counter == 3:
                    self.information3 = (skillInfo, self.game.WHITE)
            else:
                skillInfo = Fighters.battle.enemyAction(
                    self.nameToEnemy(eachEntity))
                if counter == 1:
                    self.information1 = (skillInfo, self.game.RED)
                elif counter == 2:
                    self.information2 = (skillInfo, self.game.RED)
                elif counter == 3:
                    self.information3 = (skillInfo, self.game.RED)
                if (self.protag.getCurrHealth() <= 0):
                    self.defeat = gameOverMenu(self.game, skillInfo)
                    self.game.curr_menu = self.defeat
                    self.run_display = False
                    break
            counter += 1

    def nameToEnemy(self, name):
        for eachEnemy in self.battleTroop:
            if eachEnemy.getName() == name:
                return eachEnemy
        return None

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
                    self.skillState = self.cursor_two_options(self.cursor_rect, self.skillState, 0, 1,
                                                              self.mid_w-220+self.offset, self.mid_w-50+self.offset, self.mid_h+60, self.mid_h+60)
                elif self.skillState == 1:
                    self.skillState = self.cursor_two_options(self.cursor_rect, self.skillState, 1, 2,
                                                              self.mid_w-50+self.offset, self.mid_w+120+self.offset, self.mid_h+60, self.mid_h+60)
                elif self.skillState == 2:
                    self.skillState = self.cursor_two_options(self.cursor_rect, self.skillState, 2, 3,
                                                              self.mid_w+120+self.offset, self.mid_w+290+self.offset, self.mid_h+60, self.mid_h+60)
                elif self.skillState == 3:
                    self.skillState = self.cursor_two_options(self.cursor_rect, self.skillState, 3, 0,
                                                              self.mid_w+290+self.offset, self.mid_w-220+self.offset, self.mid_h+60, self.mid_h+60)
            if self.game.LEFT_KEY:
                menuHoverSound.play()
                if self.skillState == 0:
                    self.skillState = self.cursor_two_options(self.cursor_rect, self.skillState, 0, 3,
                                                              self.mid_w-220+self.offset, self.mid_w+290+self.offset, self.mid_h+60, self.mid_h+60)
                elif self.skillState == 1:
                    self.skillState = self.cursor_two_options(self.cursor_rect, self.skillState, 1, 0,
                                                              self.mid_w-50+self.offset, self.mid_w-220+self.offset, self.mid_h+60, self.mid_h+60)
                elif self.skillState == 2:
                    self.skillState = self.cursor_two_options(self.cursor_rect, self.skillState, 2, 1,
                                                              self.mid_w+120+self.offset, self.mid_w-50+self.offset, self.mid_h+60, self.mid_h+60)
                elif self.skillState == 3:
                    self.skillState = self.cursor_two_options(self.cursor_rect, self.skillState, 3, 2,
                                                              self.mid_w+290+self.offset, self.mid_w+120+self.offset, self.mid_h+60, self.mid_h+60)
            if self.game.BACK_KEY:
                self.skillState = 0
                menuBackSound.play()
                self.reinitialize()
                self.cursor_rect.midtop = (
                    self.attackx + self.offset, self.attacky)
            if self.game.START_KEY:
                menuConfirmSound.play()
                # self.show_skills = False
                # self.attack(globalVariables.equippedSkills[self.skillState])
                self.cursor_rect.midtop = (
                    self.mid_w-180 + self.offset, self.mid_h-210)
                self.use_skill = True
        elif self.game.BACK_KEY:
            menuBackSound.play()
            self.cursor_rect.midtop = (
                self.attackx + self.offset, self.attacky)
            self.reinitialize()
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
                    self.mid_w-180 + self.offset, self.mid_h-210)
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
