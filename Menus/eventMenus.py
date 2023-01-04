from . import menu
import random
from . import battleMenu

# This file handles all the events that are not battles

# This is the directions menu, where the player can choose the next event to go to.


class directionsMenu(menu.Menu):
    def __init__(self, game):
        menu.Menu.__init__(self, game)
        # tuples containing message descriptor and the menu it connects to
        fieldMonsters = [self.deepCopyEnemy("Slime"), self.deepCopyEnemy(
            "Unicorn"), self.deepCopyEnemy("Ghost"), self.deepCopyEnemy("Spider"), self.deepCopyEnemy("Bat"), self.deepCopyEnemy("Wolf"), self.deepCopyEnemy("Skeleton")]
        cemetery = ("There is a cemetery this way. You can see ghosts and skeletons around.", battleMenu.BattleMenu(
            self.game, [self.deepCopyEnemy("Ghost"), self.deepCopyEnemy("Skeleton")], 2))
        cavern = ("There is a cavern this way. You can see slimes and spiders walking through the cave.", battleMenu.BattleMenu(
            self.game, [self.deepCopyEnemy("Slime"), self.deepCopyEnemy("Spider")], 2))
        waterfall = ("There is a waterfall this way. There are unicorns and slimes.", battleMenu.BattleMenu(
            self.game, [self.deepCopyEnemy("Slime"), self.deepCopyEnemy("Unicorn")], 2))
        openField = ("There is an open field with a variety of monsters roaming.", battleMenu.BattleMenu(
            self.game, fieldMonsters, 2))
        den = ("There is a den this way. There are wolves and bats.", battleMenu.BattleMenu(
            self.game, [self.deepCopyEnemy("Wolf"), self.deepCopyEnemy("Bat")], 2))
        campsite = (
            "There is a campsite this way. You could heal your health or mana here.", campsiteMenu(self.game))
        skills = (
            "There seems to be a skill you can pick up this way.", findSkillMenu(self.game))
        doctor = (
            "There is a doctor this way. She could help you deal with ailments.", doctorMenu(self.game))
        blackSmith = (
            "There is a blacksmith this way. He could modify your equipment.", smithMenu(self.game))
        swamp = (
            "There is a swamp this way. It could be poisonous or healing. Influenced by luck stat.", swampMenu(self.game))
        possibleEvents = [cemetery, cavern, campsite,
                          waterfall, doctor, swamp, openField, skills, blackSmith, den]

        # for future reference, we can add more stages as the player increases level.
        # if self.protag.getLevel() >= 4:
        #    possibleEvents.append()

        # pick two random events as choices for the player to go to
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
            self.menuHoverSound.play()
            self.eventState = self.cursor_two_options(self.cursor_rect, self.eventState, 0, 1,
                                                      self.mid_w-300+self.offset-40, self.mid_w+300+self.offset-40, self.mid_h+300, self.mid_h+300)
        if self.game.START_KEY:
            self.menuConfirmSound.play()
            self.game.curr_menu = self.events[self.eventState][1]
            self.run_display = False


# deals with the event in which the player can find a random skill and replace one of their skills
class findSkillMenu(menu.Menu):
    def __init__(self, game):
        menu.Menu.__init__(self, game)
        self.skillState = 0

    def display_menu(self):
        self.run_display = True
        self.cursor_rect.midtop = (
            self.mid_w-220 + self.offset, self.mid_h+60)
        # skills that you can find in this menu
        selectableSkills = [self.skills.charge, self.skills.bullseye, self.skills.tsunami,
                            self.skills.cleanse, self.skills.iceSlash, self.skills.telekinesis, self.skills.healra]
        self.randSkill = random.choice(selectableSkills)
        self.ignore = False
        while self.run_display:
            self.game.check_events()
            self.check_input()
            incrementer = 0
            self.game.display.blit(self.backMenu, (0, 0))
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
            self.game.draw_text(self.randSkill.getName(), 50, self.mid_w,
                                self.mid_h-300, self.randSkill.getColor())
            self.game.draw_text("Mana: " + str(self.randSkill.getEnergy()), 35, self.mid_w,
                                self.mid_h-240, self.game.BLACK)
            self.game.draw_text("Type: " + self.randSkill.getSkillType(), 35, self.mid_w,
                                self.mid_h-180, self.game.BLACK)
            self.game.draw_text(self.randSkill.getDescription(), 35, self.mid_w,
                                self.mid_h-120, self.game.WHITE)
            self.game.draw_text("You found a skill! Choose a skill to replace.", 60, self.mid_w,
                                self.mid_h-450, self.game.WHITE)
            self.game.draw_text("Ignore", 60, self.mid_w,
                                self.mid_h+400, self.game.WHITE)
            self.draw_cursor()
            self.blit_screen(self.game.display)

    def check_input(self):
        if self.game.RIGHT_KEY:
            self.menuHoverSound.play()
            self.skillState = self.cursor_mult_options(
                self.skillState, self.mid_w-220+self.offset, self.mid_h+60, 170, 0, 4, False)
        if self.game.LEFT_KEY:
            self.menuHoverSound.play()
            self.skillState = self.cursor_mult_options(
                self.skillState, self.mid_w-220+self.offset, self.mid_h+60, 170, 0, 4, True)
        if self.game.DOWN_KEY:
            self.menuHoverSound.play()
            self.cursor_rect.midtop = (
                self.mid_w + self.offset-50, self.mid_h+400)
            self.skillState = 0
            self.ignore = True
        if self.game.UP_KEY:
            self.menuHoverSound.play()
            self.cursor_rect.midtop = (
                self.mid_w-220 + self.offset, self.mid_h+60)
            self.skillState = 0
            self.ignore = False
        if self.game.START_KEY:
            self.menuConfirmSound.play()
            if self.ignore:
                self.game.curr_menu = directionsMenu(self.game)
                self.run_display = False
            else:
                self.protag.adjustSkills(self.skillState, self.randSkill)
                self.game.curr_menu = directionsMenu(self.game)
                self.run_display = False

# deals with the event in which the player stumbles on a swamp and either gets poisoned or healed depending on their luck


class swampMenu(menu.Menu):
    def __init__(self, game):
        menu.Menu.__init__(self, game)
        self.state = 0
        # luck increases chance of lucky event

    def display_menu(self):
        self.run_display = True
        self.cursor_rect.midtop = (
            self.mid_w + self.offset-50, self.mid_h+400)
        # generate the chance of getting a poisonous or miraculous swamp, based on player's luck stat.
        self.randDecimal = random.random() + (self.protag.luck/100)
        flag = False
        if self.protag.getCure() == True:
            flag = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.backMenu, (0, 0))
            self.draw_info()
            self.game.draw_text("Swamp", 60, self.mid_w,
                                self.mid_h-450, self.game.WHITE)
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
            self.menuConfirmSound.play()
            self.game.curr_menu = directionsMenu(self.game)
            self.run_display = False

# deals with the event in which the player can find a blacksmith to strengthen their armor or weapon with a random element.


class smithMenu(menu.Menu):
    def __init__(self, game):
        menu.Menu.__init__(self, game)
        self.state = 0

    def display_menu(self):
        self.run_display = True
        self.cursor_rect.midtop = (
            self.mid_w+self.offset-300, self.mid_h+300)
        elements = ["Fire", "Water", "Ice",
                    "Electric", "Holy", "Dark", "Strike"]
        self.randChoice1 = random.choice(elements)
        self.randChoice2 = random.choice(elements)
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.backMenu, (0, 0))
            self.draw_info()
            self.game.draw_text("Blacksmith", 60, self.mid_w,
                                self.mid_h-450, self.game.WHITE)
            self.game.draw_text("You run into a blacksmith who can alter equipment.", 50, self.mid_w,
                                self.mid_h+50, self.game.WHITE)
            self.game.draw_text("Infusion (Give your weapon " + self.randChoice1 + " infusion.)", 40, self.mid_w,
                                self.mid_h+300, self.game.WHITE)
            self.game.draw_text("Fortify (Give your armor " + self.randChoice2 + " resistance.)", 40, self.mid_w,
                                self.mid_h+400, self.game.WHITE)
            self.draw_cursor()
            self.blit_screen(self.game.display)

    def check_input(self):
        if self.game.DOWN_KEY or self.game.UP_KEY:
            self.menuHoverSound.play()
            self.state = self.cursor_two_options(
                self.cursor_rect, self.state, 0, 1, self.mid_w+self.offset-300, self.mid_w+self.offset-300, self.mid_h+300, self.mid_h + 400)
        if self.game.START_KEY:
            self.menuConfirmSound.play()
            if self.state == 0:
                self.protag.getWeapon().setElement(self.randChoice1)
                self.skills.basicAttack.adjustElement(self.randChoice1)
            else:
                self.protag.setResistances(self.randChoice2, 0.7)
            self.game.curr_menu = directionsMenu(self.game)
            self.run_display = False

# deals with the event in which the player can find a doctor to prevent a future status ailment or instantly cure a current one


class doctorMenu(menu.Menu):
    def __init__(self, game):
        menu.Menu.__init__(self, game)
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
            self.game.draw_text("Doctor", 60, self.mid_w,
                                self.mid_h-450, self.game.WHITE)
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
            self.menuHoverSound.play()
            self.state = self.cursor_two_options(
                self.cursor_rect, self.state, 0, 1, self.mid_w+self.offset-360, self.mid_w+self.offset-360, self.mid_h+300, self.mid_h + 400)
        if self.game.START_KEY:
            self.menuConfirmSound.play()
            if self.state == 0:
                self.protag.resetState()
            else:
                self.protag.setCure(True)
            self.game.curr_menu = directionsMenu(self.game)
            self.run_display = False

# deals with the event in which the player can heal at a campsite


class campsiteMenu(menu.Menu):
    def __init__(self, game):
        menu.Menu.__init__(self, game)
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
            self.game.draw_text("Campsite", 60, self.mid_w,
                                self.mid_h-450, self.game.WHITE)
            self.game.draw_text("Eat Food (Restores 250 Health)", 40, self.mid_w,
                                self.mid_h+300, self.game.WHITE)
            self.game.draw_text("Sleep (Restores 100 Mana)", 40, self.mid_w,
                                self.mid_h+400, self.game.WHITE)
            self.draw_cursor()
            self.blit_screen(self.game.display)

    def check_input(self):
        if self.game.DOWN_KEY or self.game.UP_KEY:
            self.menuHoverSound.play()
            self.state = self.cursor_two_options(
                self.cursor_rect, self.state, 0, 1, self.mid_w+self.offset-170, self.mid_w+self.offset-170, self.mid_h+300, self.mid_h + 400)
        if self.game.START_KEY:
            self.menuConfirmSound.play()
            if self.state == 0:
                self.protag.adjustHealth(250)
            else:
                self.protag.adjustEnergy(100)
            self.game.curr_menu = directionsMenu(self.game)
            self.run_display = False
