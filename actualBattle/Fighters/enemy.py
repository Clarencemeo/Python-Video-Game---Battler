import random
from random import randint


class Enemy:
    def __init__(self, health, skillDictionary, dropsDictionary, name, goldReward, experienceReward, speed, attackDamage, magicDamage,
                 physicalDefense, magicDefense, elementalResistances):
        self.health = health
        self.skillDictionary = skillDictionary
        self.dropsDictionary = dropsDictionary
        self.name = name
        self.energy = 100
        self.goldReward = goldReward
        self.experienceReward = experienceReward
        self.speed = speed
        self.turnGauge = 0
        self.attackDamage = attackDamage
        self.magicDamage = magicDamage
        self.physicalDefense = physicalDefense
        self.magicDefense = magicDefense
        self.elementalResistances = elementalResistances

    def adjustHealth(self, health):
        self.health += health

    # we're actually not ever checking the monsters energy,
    # this is just to make things smooth when making the functions
    # that execute skills.
    def adjustNegativeEnergy(self, energy):
        self.energy -= energy

    def getName(self):
        return self.name

    def modifyName(self, numberName):
        self.name = self.name + str(numberName)

    def getHealth(self):
        return self.health

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
