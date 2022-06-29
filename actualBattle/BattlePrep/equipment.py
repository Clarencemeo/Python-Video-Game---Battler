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

    def getElement(self):
        return self.element

    def getScope(self):
        return self.scope


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
