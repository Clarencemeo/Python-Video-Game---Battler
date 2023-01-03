from . import menu
from . import mainMenus
from . import eventMenus


class LevelUpMenu(menu.Menu):
    def __init__(self, game, expGained):
        menu.Menu.__init__(self, game)
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
            self.game.draw_text("You earned " + str(self.expGained) + " EXP and leveled up to level " + str(self.protag.getLevel()) + "! Choose which stats to level.", 40, self.mid_w,
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
            self.menuConfirmSound.play()
            self.run_display = False
        elif self.game.BACK_KEY:
            self.menuBackSound.play()
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
            self.menuConfirmSound.play()
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
            self.menuHoverSound.play()
            self.statState = self.cursor_mult_options(
                self.statState, cursorXpos, self.mid_h-250, 0, 70, 6, False)
        elif self.game.UP_KEY:
            self.menuHoverSound.play()
            self.statState = self.cursor_mult_options(
                self.statState, cursorXpos, self.mid_h-250, 0, 70, 6, True)


class VictoryMenu(menu.Menu):
    def __init__(self, game, expGained):
        menu.Menu.__init__(self, game)
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
            self.menuConfirmSound.play()
            self.game.curr_menu = eventMenus.directionsMenu(self.game)
            self.run_display = False


class gameOverMenu(menu.Menu):
    def __init__(self, game, finishingBlow):
        menu.Menu.__init__(self, game)
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
            self.menuConfirmSound.play()
            self.restart = mainMenus.MainMenu(self.game)
            self.game.curr_menu = self.restart
            self.run_display = False


class classMenu(menu.Menu):
    def __init__(self, game):
        menu.Menu.__init__(self, game)
        self.classState = 0
        self.classList = self.classes.listClasses

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
            self.menuHoverSound.play()
            self.classState = self.cursor_mult_options(
                self.classState, cursorXpos, self.mid_h-(250), 0, 100, 4, False)
        if self.game.UP_KEY:
            self.menuHoverSound.play()
            self.classState = self.cursor_mult_options(
                self.classState, cursorXpos, self.mid_h-(250), 0, 100, 4, True)
        if self.game.START_KEY:
            self.menuConfirmSound.play()
            menu.protagonist = self.classList[self.classState]
            self.game.curr_menu = eventMenus.directionsMenu(self.game)
            self.run_display = False
