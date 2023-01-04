import random
from random import randint
from Fighters.player import Player
from Fighters.enemy import Enemy


class Skill:
    def __init__(self, name, description, baseDmg, variationDmg, scope, energyCost, element, skillType, color):
        # scope: determines if the target is one or multiple enemies
        # skillType: determines if the Skill is magical or physical, or unique
        # color is the color of the skill when displayed in the menu
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

# Check for Unique Skills
        # Conversion skills convert mana into health or vice versa
        if self.skillType == "Conversion":
            healthChange = int(-1*(user.currHealth * 0.10))
            manaChange = int(1*(user.energy * 0.30))
            user.adjustHealth(healthChange)
            user.adjustEnergy(manaChange)
            return user.getName() + " used " + self.getName() + " ! Gained " + str(manaChange) + " mana and lost " + str(healthChange) + " health!"
        # Buff skills buff the user. as of right now, there is only one buff called Charged
        elif self.skillType == "Buff":
            user.setBuffs("Charged")
            return (user.getName() + " used " + self.getName() + " and gained the " + self.getElement() + " buff!")
        # 1Hit or Bullseye are unique skills that have a percent chance to insta-KO an enemy based on your luck
        elif self.getName() == "1Hit" or self.getName() == "Bullseye":
            self.randDecimal = random.random() + (user.luck/100)
            if self.randDecimal >= (1-(self.getBase()/100)):
                target.adjustHealth(-300)
                return (user.getName() + " used " + self.getName() + " and successfully dealt a killing blow!")
            else:
                return (user.getName() + " used " + self.getName() + " but missed!")
        # Cleanse skills can remove status ailments off of you
        elif self.skillType == "Cleanse":
            user.resetState()
            return (user.getName() + " used " + self.getName() + " and removed their stat ailments!")
        # Drain skills are unique to enemies and damage the player while healing the attacker
        elif self.skillType == "Drain":
            if self.getName() == "Draining Bite":
                target.adjustEnergy(-1 * rawDamage)
                return(user.getName() + " used " + self.getName() + " and stole " + str(rawDamage) + " mana from you!")
            else:
                target.adjustHealth(-1 * rawDamage)
                user.adjustHealth(1 * rawDamage)
                return(user.getName() + " used " + self.getName() + " and stole " + str(rawDamage) + " health from you!")
        # Status ailments have differing effects, but may be prevented with the doctor's preventative cure
        elif self.skillType == "Ailment":
            if target.getCure() == True:
                target.setCure(False)
                return (user.getName() + " attempted to use " + self.getName() + " but it was deflected by the doctor's preventative cure!")
            target.setState((self.getElement()), self.getBase())
            return(user.getName() + " used " + self.getName() + " and inflicted " + self.getElement() + " on " + target.getName() + " for " + str(self.getBase()) + " turns!")
# Check for Unique Skills - END

        # Calculate damage based on resistances and damage
        elif self.getName() == "Mystic":
            overallDamage = int((rawDamage + user.attackDamage -
                                 target.magicDefense) * target.elementalResistances[self.element])
        elif self.skillType == 'Physical':
            overallDamage = int((rawDamage + user.attackDamage -
                                 target.physicalDefense) * target.elementalResistances[self.element])
        elif self.skillType == 'Magical':
            overallDamage = int((rawDamage + user.magicDamage -
                                 target.magicDefense) * target.elementalResistances[self.element])
        elif self.skillType == 'Healing':
            healingVal = self.getBase()
            target.adjustHealth(healingVal)
            return(user.getName() + " healed " + target.getName() + " for " + str(healingVal) + " health!")
        if "Charged" == user.getBuffs():
            overallDamage = overallDamage*2.5
        # below conditional statement is used to calculate if the hit is a critical strike
        if (random.uniform(0, 1) <= user.criticalRate):
            overallDamage *= 2
            flagCrit = True
        if (self.getName() == "Gamble"):
            self.adjustElement(random.choice(
                ["Fire", "Ice", "Dark", "Light", "Water", "Strike", "Electric"]))
        # the two below conditional statements are used to calculate elemental resistances
        if (target.elementalResistances[self.element] <= 0.9):
            flagStrength = True
        if (target.elementalResistances[self.element] >= 1.1):
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
                printer = ("Used " + self.getName() + ". CRITICAL and weakpoint! You dealt " + str(overallDamage) + " " + self.getElement() +
                           " damage to the enemy " + target.name + "!")
            if (flagCrit):
                printer = ("Used " + self.getName() + ". CRITICAL! You dealt " + str(overallDamage) + " " + self.getElement() +
                           " damage to the enemy " + target.name + "!")
            elif (flagWeakness):
                printer = ("Used " + self.getName() + ". Enemy is weak to " + self.element + "! You dealt " + str(overallDamage) + " " + self.getElement() +
                           " damage to the enemy " + target.name + "!")
            elif (flagStrength):
                printer = ("Used " + self.getName() + ". Enemy resists " + self.element + "! You dealt " + str(overallDamage) + " " + self.getElement() +
                           " damage to the enemy " + target.name + "!")
            else:
                printer = ("Used " + self.getName() + ". You dealt " + str(overallDamage) + " " + self.getElement() +
                           " damage to the enemy " + target.name + "!")
            # time.sleep in order to give the user time to read the output
            if "Charged" == user.getBuffs():
                user.resetBuffs()
                return "Consumed Charge! " + printer
        if (isinstance(user, Enemy)):
            if (flagCrit and flagWeakness):
                printer = (user.getName() + " used " + self.getName() + ". CRITICAL and weakpoint! It dealt " + str(overallDamage) + " " + self.getElement() +
                           " damage to you!")
            if (flagCrit):
                printer = (user.getName() + " used " + self.getName() + ". CRITICAL! It dealt " + str(overallDamage) + " " + self.getElement() +
                           " damage to you!")
            elif (flagWeakness):
                printer = (user.getName() + " used " + self.getName() + ". It hit your weakness! It dealt " + str(overallDamage) + " " + self.getElement() +
                           " damage to you!")
            elif (flagStrength):
                printer = (user.getName() + " used " + self.getName() + ". You resist " + self.element + "! It dealt " + str(overallDamage) + " " + self.getElement() +
                           " damage to you!")
            else:
                printer = (user.getName() + " used " + self.getName() + ". It dealt " + str(overallDamage) + " " + self.getElement() +
                           " damage to you!")
        return printer
