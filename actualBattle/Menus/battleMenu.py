import os
import random
import pygame
from . import menu
from . import setupMenus
from Fighters import battle


class BattleMenu(menu.Menu):
    def __init__(self, game, monsterList, amount):
        menu.Menu.__init__(self, game)
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
        self.battleTroop = battle.assembleBattleTroop(monsterList, amount)
        self.information1 = ("", self.game.BLACK)
        self.information2 = ("", self.game.BLACK)
        self.information3 = ("", self.game.BLACK)
        self.information4 = ("", self.game.BLACK)
        self.expGained = 0
        self.defeatMessage = 0
        self.skipEnemySelection = ["Healing", "Cleanse", "Buff", "Conversion"]

    def winBattle(self):
        if len(self.battleTroop) == 0:
            # if level up, go to levelup menu, else go to victoryMenu
            if battle.levelUpCalculation(self.protag, self.expGained):
                self.levelUp = setupMenus.LevelUpMenu(
                    self.game, self.expGained)
                self.game.curr_menu = self.levelUp
            else:
                self.victory = setupMenus.VictoryMenu(
                    self.game, self.expGained)
                self.game.curr_menu = self.victory
            self.run_display = False

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
            self.menuErrorSound.play()
            self.state2 = "Enemy1"
            self.cursor_rect.midtop = (
                self.attackx + self.offset, self.attacky)
            self.reinitialize()
            return
        elif skill.getSkillType() in self.skipEnemySelection:
            self.player_turn = False
            self.attackTurnOrder(enemyTarget, skill)
            self.player_turn = True
            self.cursor_rect.midtop = (
                self.attackx + self.offset, self.attacky)
            self.reinitialize()
        elif self.game.RIGHT_KEY or self.game.LEFT_KEY:
            if (len(self.battleTroop) >= 2):
                self.menuHoverSound.play()
                self.state2 = self.cursor_two_options(
                    self.cursor_rect, self.state2, "Enemy1", "Enemy2", position_of_enemy1X, self.mid_w + self.offset, position_of_enemy1Y, self.mid_h-210)
            else:
                pass
        elif self.game.START_KEY:
            self.menuConfirmSound.play()
            if self.state2 == "Enemy1":
                enemyTarget = self.battleTroop[0]
            elif self.state2 == "Enemy2":
                enemyTarget = self.battleTroop[1]
            self.player_turn = False
            self.attackTurnOrder(enemyTarget, skill)
            self.player_turn = True
        elif self.game.BACK_KEY:
            self.menuBackSound.play()
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
            self.defeat = setupMenus.gameOverMenu(self.game, deathInfo)
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
                if skill.getSkillType() in self.skipEnemySelection:
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
                    self.defeat = setupMenus.gameOverMenu(self.game, skillInfo)
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
            self.attack(self.skills.basicAttack)
        # this is to manage the cursor when the skill menu is open.
        elif self.use_skill and self.player_turn:
            self.attack(self.protag.getSkills()[self.skillState])
        # toggles between skills when opening skill menu
        elif self.show_skills and self.player_turn:
            if self.game.RIGHT_KEY:
                self.menuHoverSound.play()
                self.skillState = self.cursor_mult_options(
                    self.skillState, self.mid_w-220+self.offset, self.mid_h+60, 170, 0, 4, False)
            if self.game.LEFT_KEY:
                self.menuHoverSound.play()
                self.skillState = self.cursor_mult_options(
                    self.skillState, self.mid_w-220+self.offset, self.mid_h+60, 170, 0, 4, True)
            if self.game.BACK_KEY:
                self.skillState = 0
                self.menuBackSound.play()
                self.reinitialize()
                self.cursor_rect.midtop = (
                    self.attackx + self.offset, self.attacky)
            if self.game.START_KEY:
                self.menuConfirmSound.play()
                # self.show_skills = False
                # self.attack(globalVariables.equippedSkills[self.skillState])
                if self.protag.skillList[self.skillState].getSkillType() in self.skipEnemySelection:
                    pass
                else:
                    self.cursor_rect.midtop = (
                        self.mid_w-180 + self.offset, self.mid_h-210)
                self.use_skill = True
        elif self.game.BACK_KEY:
            self.menuBackSound.play()
            self.cursor_rect.midtop = (
                self.attackx + self.offset, self.attacky)
            self.reinitialize()
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            self.menuHoverSound.play()
            self.state = self.cursor_two_options(
                self.cursor_rect, self.state, 'Attack', "Skills", self.attackx + self.offset, self.skillsx + self.offset, self.attacky, self.skillsy)
        elif self.game.START_KEY:
            self.menuConfirmSound.play()
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
