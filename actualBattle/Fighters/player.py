class Player:
    def __init__(self, ad, mdmg, pd, mdef, luck, speed, energy, currEnergy, health, currHealth, gold, experience, level, weapon, armor, skills, elementalResistances):
        self.energy = energy
        # currEnergy was not in original saveData
        self.currEnergy = currEnergy
        self.health = health
        self.currHealth = currHealth
        self.gold = gold
        self.weapon = weapon
        self.armor = armor
        self.experience = experience
        self.level = level
        # records status state; tuple of the form ("Status", duration)
        self.state = ["", 9]
        # "Charged"
        self.buffs = ""
        self.turnGauge = 0
        self.preventativeCure = False
        self.skillList = skills
        self.luck = luck + armor.luck
        self.criticalRate = 0.05 + weapon.criticalRate + (self.luck/100)
        self.speed = speed + weapon.speed + armor.speed
        self.attackDamage = int((ad + weapon.attackDamage) * 1.6)
        self.magicDamage = int((mdmg + weapon.magicDamage) * 1.6)
        self.physicalDefense = int((pd + armor.physicalDefense) * 1.6)
        self.magicDefense = int((mdef + armor.magicDefense) * 1.6)
        # elemental resistance is mostly based on the armor
        self.elementalResistances = {'Fire': 0+armor.elementalResistances['Fire'],
                                     'Water': 0+armor.elementalResistances['Water'],
                                     'Electric': 0+armor.elementalResistances['Electric'],
                                     'Ice': 0+armor.elementalResistances['Ice'],
                                     'Dark': 0+armor.elementalResistances['Dark'],
                                     'Light': 0+armor.elementalResistances['Light'],
                                     'Strike': 0+armor.elementalResistances['Strike']
                                     }

    def adjustHealth(self, health):  # Health adjustments can be positive or negative
        self.currHealth += health
        if self.currHealth > self.health:
            self.currHealth = self.health

    def restoreAll(self):
        self.currHealth = self.health

    def adjustEnergy(self, energy):  # Mana adjustments can be positive or negative
        self.currEnergy += energy
        if self.currEnergy > self.energy:
            self.currEnergy = self.energy
        if self.currEnergy < 0:
            self.currEnergy = 0

    def adjustNegativeEnergy(self, energy):
        self.currEnergy -= energy

    def getName(self):
        return "Player"

    def setBuffs(self, buff):
        self.buffs = buff

    def setCure(self, val):  # val is bool
        self.preventativeCure = val

    def getBuffs(self):
        return self.buffs

    def resetBuffs(self):
        self.buffs = ""

    def decrementState(self):
        self.state[1] -= 1

    def setState(self, stateName, duration):
        self.state = [stateName, duration]

    def getState(self):
        return self.state

    def resetState(self):
        self.state = ["", 9]

    def adjustGold(self, gold):  # gold adjustments can be positive or negative
        self.gold += gold

    def changeWeapon(self, weapon):
        self.weapon = weapon

    def resetTurnGauge(self):
        self.turnGauge = 0

    def changeTurnGauge(self, value):
        self.turnGauge += value

    def getTurnGauge(self):
        return self.turnGauge

    def changeArmor(self, armor):
        self.armor = armor

    def adjustattackDamage(self, value):
        self.attackDamage += value

    def adjustmagicDamage(self, value):
        self.magicDamage += value

    def adjustDefense(self, value):
        self.physicalDefense += value

    def adjustMagDef(self, value):
        self.magicDefense += value

    def adjustSpeed(self, value):
        self.speed += value

    def adjustLuck(self, value):
        self.luck += value

    def adjustExperience(self, value):
        self.experience += value

    def adjustLevel(self, value):
        self.level += value

    def setExperience(self, value):
        self.experience = value

    def printElementalResistances(self):
        for y in self.elementalResistances:
            print(y, ':', self.elementalResistances[y])

    def getWeapon(self):
        return self.weapon

    def getCure(self):
        return self.preventativeCure

    def getArmor(self):
        return self.armor

    def getSpeed(self):
        return self.speed

    def getLuck(self):
        return self.luck

    def getHealth(self):
        return self.health

    def getCurrHealth(self):
        return self.currHealth

    def getEnergy(self):
        return self.energy

    def getCurrEnergy(self):
        return self.currEnergy

    def getAttackDamage(self):
        return self.attackDamage

    def getMagicDamage(self):
        return self.magicDamage

    def getPhysicalDefense(self):
        return self.physicalDefense

    def getMagicalDefense(self):
        return self.magicDefense

    def getExperience(self):
        return self.experience

    def getLevel(self):
        return self.level

    def getSkills(self):
        return self.skillList
