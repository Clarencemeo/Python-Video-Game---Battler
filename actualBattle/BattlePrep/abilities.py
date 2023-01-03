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

    def getBase(self):
        return self.baseDmg

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
        # establish lower and upper bounds of damage
        rawDamage = randint(self.baseDmg-self.variationDmg,
                            self.baseDmg+self.variationDmg)
        if (isinstance(user, Player)):
            user.adjustNegativeEnergy(self.energyCost)
        if self.skillType == "Buff":
            user.setBuffs("Charged")
            return (user.getName() + " used " + self.getName() + " and gained the " + self.getElement() + " buff!")
        if self.skillType == "Cleanse":
            user.resetState()
            return (user.getName() + " used " + self.getName() + " and removed their stat ailments!")
        if self.skillType == "Drain":
            if self.getName() == "Draining Bite":
                target.adjustEnergy(-1 * rawDamage)
                return(user.getName() + " used " + self.getName() + " and stole " + str(rawDamage) + " mana from you!")
            else:
                target.adjustHealth(-1 * rawDamage)
                user.adjustHealth(1 * rawDamage)
                return(user.getName() + " used " + self.getName() + " and stole " + str(rawDamage) + " health from you!")
        elif self.skillType == "Ailment":
            if target.getCure() == True:
                target.setCure(False)
                return (user.getName() + " attempted to use " + self.getName() + " but it was deflected by the doctor's preventative cure!")
            target.setState((self.getElement()), self.getBase())
            return(user.getName() + " used " + self.getName() + " and inflicted " + self.getElement() + " on " + target.getName() + " for " + str(self.getBase()) + " turns!")
        elif self.skillType == 'Physical':
            overallDamage = int((rawDamage + user.attackDamage -
                                 target.physicalDefense) * target.elementalResistances[self.element])
            if "Charged" == user.getBuffs():
                overallDamage = overallDamage*2.5
        elif self.skillType == 'Magical':
            overallDamage = int((rawDamage + user.magicDamage -
                                 target.magicDefense) * target.elementalResistances[self.element])
            if "Charged" == user.getBuffs():
                overallDamage = overallDamage*2.5
        elif self.skillType == 'Healing':
            healingVal = 50
            target.adjustHealth(healingVal)
            return(user.getName() + " healed " + target.getName() + " for " + str(healingVal) + " health!")
        # below conditional statement is used to calculate if the hit is a critical strike
        if (random.uniform(0, 1) <= user.criticalRate):
            overallDamage *= 1.5
            flagCrit = True
        # the two below conditional statements are used to calculate elemental resistances
        if (target.elementalResistances[self.element] <= 0.5):
            flagStrength = True
        if (target.elementalResistances[self.element] >= 1.5):
            flagWeakness = True
        # below conditional statement is to make sure the damage does not go negative before the next line
        if (overallDamage < 0):
            overallDamage = 0
        target.adjustHealth(-1 * overallDamage)
        # if target.getHealth() <= 0:
        #    flagDefeated = True
        # the two below conditional statements print a statement based on if the user of the skill was the player or the enemy

        if (isinstance(user, Player)):
            if (flagCrit and flagWeakness):
                printer = ("Used " + self.getName() + ". CRITICAL and weakpoint! You dealt " + str(overallDamage) +
                           " damage to the enemy " + target.name + "!")
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
            if "Charged" == user.getBuffs():
                user.resetBuffs()
                return "Consumed Charge! " + printer
        if (isinstance(user, Enemy)):
            if (flagCrit and flagWeakness):
                printer = (user.getName() + " used " + self.getName() + ". CRITICAL and weakpoint! It dealt " + str(overallDamage) +
                           " damage to you!")
            if (flagCrit):
                printer = (user.getName() + " used " + self.getName() + ". CRITICAL! It dealt " + str(overallDamage) +
                           " damage to you!")
            elif (flagWeakness):
                printer = (user.getName() + " used " + self.getName() + ". It hit your weakness! It dealt " + str(overallDamage) +
                           " damage to you!")
            elif (flagStrength):
                printer = (user.getName() + " used " + self.getName() + ". You resist " + self.element + "! It dealt " + str(overallDamage) +
                           " damage to you!")
            else:
                printer = (user.getName() + " used " + self.getName() + ". It dealt " + str(overallDamage) +
                           " damage to you!")
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
