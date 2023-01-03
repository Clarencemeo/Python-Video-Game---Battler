from initializations import skillsEquipment
from initializations import globalVariables
import Fighters.battle
from Fighters.battle import *
from Fighters.enemy import Enemy
import pygame
import os
import random
import copy
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
        self.monsters = globalVariables.monsterList1
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
                # self.battle = BattleMenu(self.game)
                # self.game.curr_menu = self.battle
                self.game.curr_menu = classMenu(self.game)
            elif self.state == "Options":
                # self.game.curr_menu = self.game.options
                # self.game.curr_menu = self.game.inventory
                pass
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


class findSkillMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.skillState = 0

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            incrementer = 0
            selectableSkills = [skillsEquipment.fireballSpell]
            for each_skill in self.protag.getSkills():
                self.game.display.blit(self.backMenu, (0, 0))
                self.game.draw_text(self.protag.getSkills()[self.skillState].getDescription(), 40, self.mid_w,
                                    self.mid_h+10, self.game.BLACK)
                self.game.draw_text(each_skill.getName(), 40, self.mid_w-220+incrementer,
                                    self.mid_h+60, each_skill.getColor())
                self.game.draw_text("Mana: " + str(each_skill.getEnergy()), 25, self.mid_w-220+incrementer,
                                    self.mid_h+90, self.game.BLACK)
                self.game.draw_text("Type: " + each_skill.getSkillType(), 25, self.mid_w-220+incrementer,
                                    self.mid_h+120, self.game.BLACK)
                incrementer += 170
            self.game.draw_text("Found Skill: " + selectableSkills[0].getName(), 50, self.mid_w,
                                self.mid_h+-50, self.game.BLACK)
            self.draw_cursor()
            self.blit_screen(self.game.display)

    def check_input(self):
        if self.game.RIGHT_KEY:
            menuHoverSound.play()
            self.skillState = self.cursor_mult_options(
                self.skillState, self.mid_w-220+self.offset, self.mid_h+60, 170, 0, 4, False)
        if self.game.LEFT_KEY:
            menuHoverSound.play()
            self.skillState = self.cursor_mult_options(
                self.skillState, self.mid_w-220+self.offset, self.mid_h+60, 170, 0, 4, True)


class directionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        # tuples containing message descriptor and the menu it connects to
        fieldMonsters = [self.deepCopyEnemy("Slime"), self.deepCopyEnemy(
            "Unicorn"), self.deepCopyEnemy("Ghost"), self.deepCopyEnemy("Bat"), self.deepCopyEnemy("Wolf")]
        cemetery = ("There is a cemetery this way. You can see ghosts and bats flying around.", BattleMenu(
            self.game, [self.deepCopyEnemy("Ghost"), self.deepCopyEnemy("Bat")], 2))
        cavern = ("There is a cavern this way. You can see slimes and spiders walking through the cave.", BattleMenu(
            self.game, [self.deepCopyEnemy("Slime"), self.deepCopyEnemy("Slime")], 2))
        waterfall = ("There is a waterfall this way. There are unicorns and slimes.", BattleMenu(
            self.game, [self.deepCopyEnemy("Slime"), self.deepCopyEnemy("Unicorn")], 2))
        openField = ("There is an open field with a variety of monsters roaming.", BattleMenu(
            self.game, fieldMonsters, 2))
        campsite = (
            "There is a campsite this way. You could heal your health or mana here.", campsiteMenu(self.game))
        skills = (
            "There seems to be a skill you can pick up this way.", findSkillMenu(self.game))
        doctor = (
            "There is a doctor this way. She could help you deal with ailments.", doctorMenu(self.game))
        swamp = (
            "There is a swamp this way. It could be poisonous or healing. Influenced by luck stat.", swampMenu(self.game))
        # possibleEvents = [cemetery, cavern, campsite,
        #                  waterfall, doctor, swamp, openField]
        possibleEvents = [skills, campsite]
        # if self.protag.getLevel() >= 4:
        #    possibleEvents.append()
        leftEvent = random.choice(possibleEvents)
        possibleEvents.remove(leftEvent)
        rightEvent = random.choice(possibleEvents)
        self.eventState = 0
        self.events = [leftEvent, rightEvent]

    def display_menu(self):
        self.run_display = True
        self.cursor_rect.midtop = (
            self.mid_w-300+self.offset-40, self.mid_h+300)
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.backMenu, (0, 0))
            self.game.draw_text("Which way will you go?", 70, self.mid_w,
                                self.mid_h-470, self.game.BLACK)
            self.draw_info()
            self.game.draw_text("Left", 50, self.mid_w-300,
                                self.mid_h+300, self.game.WHITE)
            self.game.draw_text("Right", 50, self.mid_w+300,
                                self.mid_h+300, self.game.WHITE)
            if self.protag.getState()[0] == "Blind":
                self.game.draw_text("You are blinded and cannot see where this path leads.", 50, self.mid_w,
                                    self.mid_h+50, self.game.WHITE)
            else:
                self.game.draw_text(self.events[self.eventState][0], 50, self.mid_w,
                                    self.mid_h+50, self.game.WHITE)
            self.draw_cursor()
            self.blit_screen(self.game.display)

    def check_input(self):
        if self.game.RIGHT_KEY or self.game.LEFT_KEY:
            menuHoverSound.play()
            self.eventState = self.cursor_two_options(self.cursor_rect, self.eventState, 0, 1,
                                                      self.mid_w-300+self.offset-40, self.mid_w+300+self.offset-40, self.mid_h+300, self.mid_h+300)
        if self.game.START_KEY:
            menuConfirmSound.play()
            self.game.curr_menu = self.events[self.eventState][1]
            self.run_display = False


class swampMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 0
        # luck increases chance of lucky event

    def display_menu(self):
        self.run_display = True
        self.cursor_rect.midtop = (
            self.mid_w + self.offset-50, self.mid_h+400)
        self.randDecimal = random.random() + (self.protag.luck/100)
        flag = False
        if self.protag.getCure() == True:
            flag = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.backMenu, (0, 0))
            self.draw_info()
            if self.randDecimal <= 0.5:
                if flag:
                    self.game.draw_text("The swamp ended up being poisonous but the doctor's preventative cure deflected it!", 50, self.mid_w,
                                        self.mid_h+50, self.game.WHITE)
                    self.protag.setCure(False)
                else:
                    self.game.draw_text("The swamp ended up being poisonous and you got poisoned.", 50, self.mid_w,
                                        self.mid_h+50, self.game.WHITE)
                    self.protag.setState("Poison", 4)
            else:
                self.game.draw_text("The swamp was miraculous and fully healed your health and status ailments!", 50, self.mid_w,
                                    self.mid_h+50, self.game.WHITE)
                self.protag.restoreAll()
                self.protag.resetState()
            self.game.draw_text("Continue", 60, self.mid_w,
                                self.mid_h+400, self.game.WHITE)
            self.draw_cursor()
            self.blit_screen(self.game.display)

    def check_input(self):
        if self.game.START_KEY:
            menuConfirmSound.play()
            self.game.curr_menu = directionsMenu(self.game)
            self.run_display = False


class doctorMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 0

    def display_menu(self):
        self.run_display = True
        self.cursor_rect.midtop = (
            self.mid_w+self.offset-360, self.mid_h+300)
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.backMenu, (0, 0))
            self.draw_info()
            self.game.draw_text("You run into a doctor who specializes in status ailments!", 50, self.mid_w,
                                self.mid_h+50, self.game.WHITE)
            self.game.draw_text("Instant Cure (Heal all current status ailments)", 40, self.mid_w,
                                self.mid_h+300, self.game.WHITE)
            self.game.draw_text("Preventative Cure (Prevent the next status ailment)", 40, self.mid_w,
                                self.mid_h+400, self.game.WHITE)
            self.draw_cursor()
            self.blit_screen(self.game.display)

    def check_input(self):
        if self.game.DOWN_KEY or self.game.UP_KEY:
            menuHoverSound.play()
            self.state = self.cursor_two_options(
                self.cursor_rect, self.state, 0, 1, self.mid_w+self.offset-360, self.mid_w+self.offset-360, self.mid_h+300, self.mid_h + 400)
        if self.game.START_KEY:
            menuConfirmSound.play()
            if self.state == 0:
                self.protag.resetState()
            else:
                self.protag.setCure(True)
            self.game.curr_menu = directionsMenu(self.game)
            self.run_display = False


class campsiteMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 0

    def display_menu(self):
        self.run_display = True
        self.cursor_rect.midtop = (
            self.mid_w+self.offset-185, self.mid_h+300)
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.backMenu, (0, 0))
            self.draw_info()
            self.game.draw_text("Eat Food (Restores 250 Health)", 40, self.mid_w,
                                self.mid_h+300, self.game.WHITE)
            self.game.draw_text("Sleep (Restores 100 Mana)", 40, self.mid_w,
                                self.mid_h+400, self.game.WHITE)
            self.draw_cursor()
            self.blit_screen(self.game.display)

    def check_input(self):
        if self.game.DOWN_KEY or self.game.UP_KEY:
            menuHoverSound.play()
            self.state = self.cursor_two_options(
                self.cursor_rect, self.state, 0, 1, self.mid_w+self.offset-170, self.mid_w+self.offset-170, self.mid_h+300, self.mid_h + 400)
        if self.game.START_KEY:
            menuConfirmSound.play()
            if self.state == 0:
                self.protag.adjustHealth(250)
            else:
                self.protag.adjustEnergy(100)
            self.game.curr_menu = directionsMenu(self.game)
            self.run_display = False


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
            self.game.display.blit(self.backMenu, (0, 0))
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
            self.victory = VictoryMenu(self.game, self.expGained)
            self.game.curr_menu = self.victory
            menuConfirmSound.play()
            self.run_display = False
        elif self.game.BACK_KEY:
            menuBackSound.play()
            self.statState = 0
            self.cursor_rect.midtop = (
                self.mid_w-550 + self.offset-50, self.mid_h-250)
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
            self.statState = self.cursor_mult_options(
                self.statState, cursorXpos, self.mid_h-250, 0, 70, 6, False)
        elif self.game.UP_KEY:
            menuHoverSound.play()
            self.statState = self.cursor_mult_options(
                self.statState, cursorXpos, self.mid_h-250, 0, 70, 6, True)


class VictoryMenu(Menu):
    def __init__(self, game, expGained):
        Menu.__init__(self, game)
        self.expGained = expGained

    def display_menu(self):
        self.run_display = True
        self.cursor_rect.midtop = (
            self.mid_w + self.offset-50, self.mid_h+400)
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.backMenu, (0, 0))
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
            self.game.draw_text("Mana: " + str(self.protag.getCurrEnergy()) + "/" + str(self.protag.getEnergy()), 40, self.mid_w,
                                self.mid_h+50, self.game.BLACK)
            self.game.draw_text("Continue", 60, self.mid_w,
                                self.mid_h+400, self.game.WHITE)
            self.draw_cursor()
            self.blit_screen(self.game.display)

    def check_input(self):
        if self.game.START_KEY:
            menuConfirmSound.play()
            self.game.curr_menu = directionsMenu(self.game)
            self.run_display = False


class gameOverMenu(Menu):
    def __init__(self, game, finishingBlow):
        Menu.__init__(self, game)
        self.finishingBlow = finishingBlow

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.backMenu, (0, 0))
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


class classMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.classState = 0
        self.classList = initializations.globalVariables.classList

    def display_menu(self):
        self.run_display = True
        self.cursor_rect.midtop = (
            self.mid_w-550+self.offset-70, self.mid_h-250)
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.backMenu, (0, 0))
            self.game.draw_text("Pick your class!", 70, self.mid_w,
                                self.mid_h-470, self.game.BLACK)
            self.game.draw_text("Health: " + str(self.classList[self.classState].health), 40, self.mid_w,
                                self.mid_h-390, self.game.WHITE)
            self.game.draw_text("Mana: " + str(self.classList[self.classState].energy), 40, self.mid_w,
                                self.mid_h-320, self.game.WHITE)
            self.game.draw_text("Strength: " + str(self.classList[self.classState].attackDamage), 40, self.mid_w,
                                self.mid_h-250, self.game.WHITE)
            self.game.draw_text("Magic: " + str(self.classList[self.classState].magicDamage), 40, self.mid_w,
                                self.mid_h-180, self.game.WHITE)
            self.game.draw_text("Defense: " + str(self.classList[self.classState].physicalDefense), 40, self.mid_w,
                                self.mid_h-110, self.game.WHITE)
            self.game.draw_text("MagDef: " + str(self.classList[self.classState].magicDefense), 40, self.mid_w,
                                self.mid_h-40, self.game.WHITE)
            self.game.draw_text("Speed: " + str(self.classList[self.classState].speed), 40, self.mid_w,
                                self.mid_h+30, self.game.WHITE)
            self.game.draw_text("Luck: " + str(self.classList[self.classState].luck), 40, self.mid_w,
                                self.mid_h+100, self.game.WHITE)
            self.game.draw_text("Weapon: " + str(self.classList[self.classState].weapon.getName()), 40, self.mid_w,
                                self.mid_h+170, self.game.WHITE)
            self.game.draw_text("Armor: " + str(self.classList[self.classState].armor.getName()), 40, self.mid_w,
                                self.mid_h+240, self.game.WHITE)
            self.game.draw_text("Skills", 60, self.mid_w+450,
                                self.mid_h-250, self.game.WHITE)
            incrementer = 100
            # make sure to set .equippedSkills to whatever class you pick
            # or jsut whenever you look at skills, access the skills directly from player instead
            for each_skill in self.classList[self.classState].getSkills():
                self.game.draw_text(each_skill.getName(), 40, self.mid_w+450,
                                    self.mid_h-250+incrementer, each_skill.getColor())
                incrementer += 100
            cursorXpos = self.mid_w-550
            self.game.draw_text("Wizard", 60, cursorXpos,
                                self.mid_h-250, self.game.WHITE)
            self.game.draw_text("Warrior", 60, cursorXpos,
                                self.mid_h-150, self.game.WHITE)
            self.game.draw_text("Archer", 60, cursorXpos,
                                self.mid_h-50, self.game.WHITE)
            self.game.draw_text("Cleric", 60, cursorXpos,
                                self.mid_h+50, self.game.WHITE)
            self.draw_cursor()
            self.blit_screen(self.game.display)

    def check_input(self):
        cursorXpos = self.mid_w-550+self.offset-70
        if self.game.DOWN_KEY:
            menuHoverSound.play()
            self.classState = self.cursor_mult_options(
                self.classState, cursorXpos, self.mid_h-(250), 0, 100, 4, False)
        if self.game.UP_KEY:
            menuHoverSound.play()
            self.classState = self.cursor_mult_options(
                self.classState, cursorXpos, self.mid_h-(250), 0, 100, 4, True)
        if self.game.START_KEY:
            menuConfirmSound.play()
            initializations.globalVariables.protagonist = self.classList[self.classState]
            # self.game.curr_menu = BattleMenu(
            #    self.game, [self.monsters["Ghost"], self.monsters["Slime"]], 2)
            self.game.curr_menu = directionsMenu(self.game)
            self.run_display = False
            # tempClassState = self.classState
            # self.classState = self.cursor_two_options(
            #    self.cursor_rect, self.classState, self.classState, self.classState+1, cursorXpos, cursorXpos, self.mid_h-(250)+(tempClassState*100), self.mid_h-(250)+((tempClassState+1)*100))

            # if self.classState == 0:
            #    self.classState = self.cursor_two_options(
            #        self.cursor_rect, self.classState, 0, 1, cursorXpos, cursorXpos, self.mid_h-250, self.mid_h-150)


class BattleMenu(Menu):  # might need to pass in parameter to indicate difficulty of enemies
    def __init__(self, game, monsterList, amount):
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
        # self.battleTroop = assembleBattleTroop(globalVariables.monsterList1, 2)
        self.battleTroop = assembleBattleTroop(monsterList, amount)
        self.information1 = ("", self.game.BLACK)
        self.information2 = ("", self.game.BLACK)
        self.information3 = ("", self.game.BLACK)
        self.information4 = ("", self.game.BLACK)
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
        for i in self.battleTroop:
            self.expGained += i.getExperienceReward()
        while self.run_display:
            self.display_again()

    def display_again(self):
        self.game.check_events()
        self.check_input()
        self.game.display.blit(self.backMenu, (0, 0))
        self.winBattle()
        self.turnOrder = "Turn Order: " + self.calculate_turn_order()
        self.game.draw_text("Your Health: " + str(self.protag.getCurrHealth()), 40, self.mid_w,
                            self.mid_h-450, self.game.BLACK)
        self.game.draw_text("Your Mana: " + str(self.protag.getCurrEnergy()), 40, self.mid_w,
                            self.mid_h-400, self.game.BLACK)
        if self.protag.getState()[0] != "":
            self.game.draw_text("Ailments: " + self.protag.getState()[0] + " for " + str(self.protag.getState()[1]) + " turns", 40, self.mid_w,
                                self.mid_h-350, (229, 255, 0))
        if (len(self.battleTroop) == 1):
            self.draw_enemy(self.battleTroop[0], 180)
        elif (len(self.battleTroop) == 2):
            self.draw_enemy(self.battleTroop[0], 180)
            self.draw_enemy(self.battleTroop[1], 0)
        self.game.draw_text(
            self.information1[0], 40, self.mid_w, self.mid_h+190, self.information1[1])
        self.game.draw_text(
            self.information2[0], 40, self.mid_w, self.mid_h+230, self.information2[1])
        self.game.draw_text(
            self.information3[0], 40, self.mid_w, self.mid_h+270, self.information3[1])
        self.game.draw_text(
            self.information4[0], 40, self.mid_w, self.mid_h+310, self.information4[1])
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
            for each_skill in self.protag.getSkills():
                self.game.draw_text(self.protag.getSkills()[self.skillState].getDescription(), 40, self.mid_w,
                                    self.mid_h+10, self.game.BLACK)
                self.game.draw_text(each_skill.getName(), 40, self.mid_w-220+incrementer,
                                    self.mid_h+60, each_skill.getColor())
                self.game.draw_text("Mana: " + str(each_skill.getEnergy()), 25, self.mid_w-220+incrementer,
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
        if self.protag.getState()[0] == "Blind":
            self.game.draw_text(
                "Health: ???", 30, self.mid_w-xOffset, self.mid_h-170, self.game.BLACK)
        else:
            self.game.draw_text(
                "Health: " + enemy.getStringHealth(), 30, self.mid_w-xOffset, self.mid_h-170, self.game.BLACK)
        self.game.display.blit(
            pygame.transform.scale(pygame.image.load(
                os.path.join('Assets', enemy.getOriginalName() + ".png")), (125, 125)), (self.mid_w-xOffset-60, self.mid_h-130))

    def reinitialize(self):
        self.state = "Attack"
        self.state2 = "Enemy1"
        self.skillState = 0
        self.cursor_on_enemies = False
        self.show_skills = False
        self.use_skill = False

    def calculate_turn_order(self):
        self.speedDict = {}
        playerSpeed = self.protag.speed
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
        enemyTarget = ""
        if (skill.getEnergy() > self.protag.getCurrEnergy()):
            menuErrorSound.play()
            self.state2 = "Enemy1"
            self.cursor_rect.midtop = (
                self.attackx + self.offset, self.attacky)
            self.reinitialize()
            return
        elif (skill.getSkillType() == "Healing" or skill.getSkillType() == "Cleanse" or skill.getSkillType() == "Buff"):
            self.player_turn = False
            self.attackTurnOrder(enemyTarget, skill)
            self.player_turn = True
            self.cursor_rect.midtop = (
                self.attackx + self.offset, self.attacky)
            self.reinitialize()
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

    def checkPoison(self):
        if self.protag.getState()[0] == "Poison":
            self.protag.adjustHealth(-1*(0.10*self.protag.health))
            self.protag.decrementState()
            self.checkDefeat("You died from poison.")
            return True
            return ("You took " + str(0.10*self.protag.health) + " damage from poison.")

    def checkSilence(self):
        if self.protag.getState()[0] == "Silence":
            self.protag.decrementState()
            return True

    def checkBlind(self):
        if self.protag.getState()[0] == "Blind":
            self.protag.decrementState()
            return True

    def checkAllAilments(self):
        poison = self.checkPoison()
        silence = self.checkSilence()
        blind = self.checkBlind()
        if poison:
            return ("You took " + str(0.10*self.protag.health) + " damage from poison.")
        if silence:
            return ("You are silenced and can only use physical attacks or skills.")
        if blind:
            return ("You are blinded and cannot see your enemy's health.")
        return ""

    def checkDefeat(self, deathInfo):
        if (self.protag.getCurrHealth() <= 0):
            self.defeat = gameOverMenu(self.game, deathInfo)
            self.game.curr_menu = self.defeat
            self.run_display = False
            return True
        return False

    def attackTurnOrder(self, enemyTarget, skill):
        counter = 1
        self.information1 = ("", self.game.BLACK)
        self.information2 = ("", self.game.BLACK)
        self.information3 = ("", self.game.BLACK)
        for eachEntity in self.turnList:
            if eachEntity == "Player":
                if skill.getSkillType() == "Healing" or skill.getSkillType() == "Cleanse" or skill.getSkillType() == "Buff":
                    skillInfo = skill.executeSkill(
                        self.protag, self.protag)
                else:
                    if(self.protag.getState()[0] == "Silence" and skill.getSkillType() != "Physical"):
                        skillInfo = "You tried to use a non-physical skill, but you were silenced!"
                    else:
                        skillInfo = skill.executeSkill(
                            enemyTarget, self.protag)
                        if (enemyTarget.getHealth() <= 0):
                            self.battleTroop.remove(enemyTarget)
                            skillInfo = "You defeated the " + enemyTarget.getName() + "!"
                            self.cursor_rect.midtop = (
                                self.mid_w-180 + self.offset, self.mid_h-210)
                            self.deleteFromList(enemyTarget.getName())
                            self.state2 = "Enemy1"
                if counter == 1:
                    self.information1 = (skillInfo, self.game.WHITE)
                elif counter == 2:
                    self.information2 = (skillInfo, self.game.WHITE)
                elif counter == 3:
                    self.information3 = (skillInfo, self.game.WHITE)
            else:
                enemy = self.nameToEnemy(
                    eachEntity)
                chosenSkill = enemy.randomSkillSelection()
                if chosenSkill.getSkillType() != "Healing":
                    skillInfo = chosenSkill.executeSkill(self.protag, enemy)
                else:
                    skillInfo = chosenSkill.executeSkill(
                        random.choice(self.battleTroop), enemy)
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
        self.information4 = (
            self.checkAllAilments(), (229, 255, 0))
        if self.protag.getState()[1] <= 0:
            self.protag.resetState()
            self.information4 = (
                "The ailment you had wore off.", (229, 255, 0))

    def nameToEnemy(self, name):
        for eachEnemy in self.battleTroop:
            if eachEnemy.getName() == name:
                return eachEnemy
        return None

    def check_input(self):
        # this is when the player uses regular attack
        if self.cursor_on_enemies and self.player_turn:
            self.attack(skillsEquipment.basicAttack)
        # this is to manage the cursor when the skill menu is open.
        elif self.use_skill and self.player_turn:
            self.attack(self.protag.getSkills()[self.skillState])
        # toggles between skills when opening skill menu
        elif self.show_skills and self.player_turn:
            if self.game.RIGHT_KEY:
                menuHoverSound.play()
                self.skillState = self.cursor_mult_options(
                    self.skillState, self.mid_w-220+self.offset, self.mid_h+60, 170, 0, 4, False)
            if self.game.LEFT_KEY:
                menuHoverSound.play()
                self.skillState = self.cursor_mult_options(
                    self.skillState, self.mid_w-220+self.offset, self.mid_h+60, 170, 0, 4, True)
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
                if self.protag.skillList[self.skillState].getSkillType() != "Healing":
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
            self.state = self.cursor_two_options(
                self.cursor_rect, self.state, 'Attack', "Skills", self.attackx + self.offset, self.skillsx + self.offset, self.attacky, self.skillsy)
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
