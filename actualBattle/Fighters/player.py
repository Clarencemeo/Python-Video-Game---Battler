class Player:
    def __init__(self, energy, currEnergy, health, currHealth, gold, experience, level, weapon, armor, skills, elementalResistances):
        self.energy = energy
        # currEnergy was not in original saveData
        self.currEnergy = currEnergy
        self.health = health + armor.health
        self.currHealth = currHealth
        self.gold = gold
        self.weapon = weapon
        self.armor = armor
        self.experience = experience
        self.level = level
        self.turnGauge = 0
        self.skillList = skills
        self.criticalRate = 0.05 + weapon.criticalRate
        self.speed = 7 + weapon.speed + armor.speed
        self.attackDamage = 5 + weapon.attackDamage
        self.magicDamage = 25 + weapon.magicDamage
        self.physicalDefense = 10 + armor.physicalDefense
        self.magicDefense = 10 + armor.magicDefense
        self.luck = 0.05 + armor.luck
        # elemental resistance is mostly based on the armor
        self.elementalResistances = {'Fire': 0+armor.elementalResistances['Fire'],
                                     'Water': 0+armor.elementalResistances['Water'],
                                     'Electric': 0+armor.elementalResistances['Electric'],
                                     'Ice': 0+armor.elementalResistances['Ice'],
                                     'Dark': 0+armor.elementalResistances['Dark'],
                                     'Light': 0+armor.elementalResistances['Light'],
                                     'Physical': 0+armor.elementalResistances['Physical']
                                     }

    def adjustHealth(self, health):  # Health adjustments can be positive or negative
        self.currHealth += health

    def adjustNegativeEnergy(self, energy):
        self.energy -= energy

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

    def getArmor(self):
        return self.armor

    def getSpeed(self):
        return self.speed

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
