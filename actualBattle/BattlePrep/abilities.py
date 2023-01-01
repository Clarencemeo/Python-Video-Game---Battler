import random
from random import randint
from Fighters.player import Player
from Fighters.enemy import Enemy
import time


class Skill:
    def __init__(self, name, description, baseDmg, variationDmg, scope, energyCost, element, skillType, color):
        # scope: determines if the target is one or multiple enemies
        # skillType: determines if the Skill is magical or physical
        self.name = name
        self.baseDmg = baseDmg
        self.variationDmg = variationDmg
        self.scope = scope
        self.energyCost = energyCost
        self.element = element
        self.skillType = skillType
        self.color = color
        self.description = description

    def getEnergy(self):
        return self.energyCost

    def getColor(self):
        return self.color

    def getDescription(self):
        return self.description

    def getName(self):
        return self.name

    def getScope(self):
        return self.scope

    def getSkillType(self):
        return self.skillType

    def getElement(self):
        return self.element

    def adjustScope(self, scope):
        self.scope = scope

    def adjustName(self, name):
        self.name = name

    def adjustElement(self, element):
        self.element = element

    def adjustSkillType(self, skilltype):
        self.skillType = skilltype

    # skill type refers to physical, magical, or neutral damage
    def executeSkill(self, target, user):
        printer = ""
        flagCrit = False
        flagWeakness = False
        flagStrength = False
        flagDefeated = False
        # establish lower and upper bounds of damage
        rawDamage = randint(self.baseDmg-self.variationDmg,
                            self.baseDmg+self.variationDmg)
        user.adjustNegativeEnergy(self.energyCost)
        if self.skillType == 'Physical':
            overallDamage = rawDamage + user.attackDamage - \
                target.physicalDefense - \
                target.elementalResistances[self.element]
        elif self.skillType == 'Magical':
            overallDamage = rawDamage + user.magicDamage - \
                target.magicDefense - \
                target.elementalResistances[self.element]
        print(overallDamage)
        # below conditional statement is used to calculate if the hit is a critical strike
        if (random.uniform(0, 1) <= user.criticalRate):
            overallDamage *= 1.5
            flagCrit = True
        # the two below conditional statements are used to calculate elemental resistances
        if (target.elementalResistances[self.element] > 5):
            flagStrength = True
        if (target.elementalResistances[self.element] < 0):
            flagWeakness = True
        # below conditional statement is to make sure the damage does not go negative before the next line
        if (overallDamage < 0):
            overallDamage = 0
        target.adjustHealth(-1 * overallDamage)
        # if target.getHealth() <= 0:
        #    flagDefeated = True
        # the two below conditional statements print a statement based on if the user of the skill was the player or the enemy

        if (isinstance(user, Player)):
            if (flagCrit):
                printer = ("Used " + self.getName() + ". CRITICAL! You dealt " + str(overallDamage) +
                           " damage to the enemy " + target.name + "!")
            elif (flagWeakness):
                printer = ("Used " + self.getName() + ". Enemy is weak to " + self.element + "! You dealt " + str(overallDamage) +
                           " damage to the enemy " + target.name + "!")
            elif (flagStrength):
                printer = ("Used " + self.getName() + ". Enemy resists " + self.element + "! You dealt " + str(overallDamage) +
                           " damage to the enemy " + target.name + "!")
            else:
                printer = ("Used " + self.getName() + ". You dealt " + str(overallDamage) +
                           " damage to the enemy " + target.name + "!")
            # time.sleep in order to give the user time to read the output
        if (isinstance(user, Enemy)):
            printer = (user.getName() + " dealt " +
                       str(overallDamage) + " damage to you with " + self.getName() + "!")
        return printer


class BuffDebuffSkill:
    def __init__(self, name, energy, stat, adjustment, skillType, color):
        self.name = name
        self.color = color
        self.energyCost = energy
        self.stat = stat  # tracks which stat in particular will be adjusted
        self.skillType = skillType  # tracks if the stat is a buff or debuff
        if (self.skillType == "Buff"):
            self.adjustment = adjustment
        else:
            self.adjustment = adjustment * -1

    def executeSkill(self, target, user):
        if (self.stat == "Attack Damage"):
            target.adjustattackDamage(self.adjustment)
        if (self.stat == "Magic Damage"):
            target.adjustmagicDamage(self.adjustment)

    def getName(self):
        return self.name

    def getColor(self):
        return self.color

    def getEnergy(self):
        return self.energyCost

    def getType(self):
        return self.skillType

    def getStat(self):
        return self.stat
