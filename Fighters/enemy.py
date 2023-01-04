import random
from random import randint

# initializations for enemies


class Enemy:
    def __init__(self, health, skillDictionary, name, goldReward, experienceReward, speed, attackDamage, magicDamage,
                 physicalDefense, magicDefense, elementalResistances, critRate, originalName):
        self.health = health
        self.maxHealth = health
        self.skillDictionary = skillDictionary
        self.name = name
        self.energy = 100
        self.goldReward = goldReward
        self.experienceReward = experienceReward
        self.speed = speed
        self.turnGauge = 0
        self.preventativeCure = False
        self.attackDamage = attackDamage
        self.magicDamage = magicDamage
        self.physicalDefense = physicalDefense
        self.magicDefense = magicDefense
        self.elementalResistances = elementalResistances
        self.criticalRate = critRate
        self.originalName = originalName
        self.state = ()

    # original name preserves the name even after
    # the other name is modified after deepCopy in the case of duplicates
    def getOriginalName(self):
        return self.originalName

    def getCure(self):
        return self.preventativeCure

    def setCure(self, val):  # val is bool
        self.preventativeCure = val

    def adjustHealth(self, health):
        self.health += health
        if self.health > self.maxHealth:
            self.health = self.maxHealth

    # we're actually not ever checking the monsters energy,
    # this is just to make things smooth when making the functions
    # that execute skills.
    def adjustNegativeEnergy(self, energy):
        self.energy -= energy

    def decrementState(self):
        self.state[1] -= 1

    def setState(self, state):
        self.state = state

    def getBuffs(self):
        pass

    def resetState(self):
        self.state = ()

    def getName(self):
        return self.name

    def modifyName(self, numberName):
        self.name = self.name + str(numberName)

    def getHealth(self):
        return self.health

    def getMaxHealth(self):
        return self.maxHealth

    def getStringHealth(self):
        return str(self.health)

    def getGoldReward(self):
        return self.goldReward

    def getExperienceReward(self):
        return self.experienceReward

    def getSpeed(self):
        return self.speed

    def resetTurnGauge(self):
        self.turnGauge = 0

    def changeTurnGauge(self, value):
        self.turnGauge += value

    def getTurnGauge(self):
        return self.turnGauge

    # given the self.skillDictionary that has each
    # skill and their percent chance of being used,
    # pick a random skill from that dictionary.

    def randomSkillSelection(self):
        skillSelection = random.randint(0, 100)
        for skill in self.skillDictionary:
            # self.skillDictionary.get(skill) returns the percent chance that the
            # enemy will use that specific skill.
            # For this to work, skillDictionary MUST be in order from least to greatest percentage.
            if (skillSelection <= self.skillDictionary.get(skill)):
                return skill
