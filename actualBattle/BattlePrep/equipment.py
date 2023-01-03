import pygame


class Weapon:
    def __init__(self, name, speed, attackDamage, magicDamage, criticalRate, element, scope):
        self.name = name
        self.speed = speed
        self.attackDamage = attackDamage
        self.magicDamage = magicDamage
        self.criticalRate = criticalRate
        self.element = element
        self.scope = scope

    def getName(self):
        return self.name

    def getSpeed(self):
        return self.speed

    def getAttackDamage(self):
        return self.attackDamage

    def getMagicDamage(self):
        return self.magicDamage

    def getCriticalRate(self):
        return self.criticalRate

    def getElement(self):
        return self.element

    def getScope(self):
        return self.scope

    def getImage(self):
        return self.image

    def setElement(self, element):
        self.element = element

    def formatDictionarySlot(self):
        return {"Name": self.name, "Speed": self.speed, "Attack Damage": self.attackDamage, "Magic Damage": self.magicDamage, "Critical Rate": self.criticalRate, "Element": self.element, "Scope": self.scope, "Image": self.image}


class Armor:
    def __init__(self, name, speed, health, physicalDefense, magicDefense, luck, elementalResistances):
        self.name = name
        self.speed = speed
        self.physicalDefense = physicalDefense
        self.health = health
        self.magicDefense = magicDefense
        self.luck = luck
        self.elementalResistances = elementalResistances

    def getName(self):
        return self.name

    def setResistances(self, element, value):
        self.elementalResistances[element] = value
