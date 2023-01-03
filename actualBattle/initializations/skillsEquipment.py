from BattlePrep.abilities import *
from BattlePrep.equipment import *

# silverSword = Weapon("Silver Sword", 5, 1, 0, 0.03,
#                     'Physical', "Single", "Assets/SilverSword.png")


class Skills:
    def __init__(self):
        # Below are the initializations for the skills, weapons, and armor.
        # Skill(Name, description, base dmg, var dmg, scope, energy cost, element, skillType, color)

        # Elemental Magic Skills
        self.fireballSpell = Skill("Fireball", "Deals low magical fire damage to one enemy.", 7.5, 2.5, "Single",
                                   8, 'Fire', "Magical", (245, 72, 66))
        self.water = Skill("Torrent", "Deals low magical water damage to one enemy.", 7.5, 2.5, "Single",
                           8, 'Water', "Magical", (0, 92, 250))
        self.darkStrike = Skill("Dark",  "Deals low magical dark damage to one enemy.", 7.5, 2.5, "Single",
                                8, 'Dark', "Magical", (97, 88, 87))
        self.freezeSpell = Skill("Ice",  "Deals low magical ice damage to one enemy.", 7.5, 2.5,
                                 "Single", 8, 'Ice', "Magical", (17, 250, 246))
        self.zap = Skill("Zap",  "Deals low magical electric damage to one enemy.", 7.5, 2.5, "Single", 8,
                         "Electric", "Magical", (235, 231, 26))
        self.holy = Skill("Holy", "Deals low magical light damage to one enemy.", 7.5, 2.5, "Single",
                          8, 'Light', "Magical", (235, 234, 176))
        self.telekinesis = Skill("Kinesis", "Deals low magical strike damage to one enemy.", 7.5, 2.5, "Single",
                                 8, 'Strike', "Magical", (0, 0, 0))
        # Elemental Magic Skills END

        # Physical Skills
        self.basicAttack = Skill("Attack",  "Attack an enemy. Effects differ based on weapon.", 6, 1, "Single", 0,
                                 "Strike", "Physical", (0, 0, 0))
        self.bluntStrike = Skill("Skewer",  "Deal moderate physical strike damage to one enemy.", 16, 5, "Single", 15,
                                 "Strike", "Physical", (0, 0, 0))
        self.electricSlash = Skill("ESlash",  "Deal low physical electric damage to one enemy.", 9, 3, "Single", 10,
                                   "Electric", "Physical", (235, 231, 26))
        self.iceSlash = Skill("Popsicle",  "Deal low physical ice damage to one enemy.", 9, 3, "Single", 10,
                              "Ice", "Physical", (17, 250, 246))
        # Physical Skills END

        # Buff & Healing Skills

        self.charge = Skill("Charge",  "Your next attack deals 2.5x more damage.", 7.5, 2.5,
                            "Single", 25, 'Charged', "Buff", (235, 234, 176))
        self.heal = Skill("Heal",  "Heal self for 50 health", 50, 0, "Single", 20,
                          "Magical", "Healing", (0, 0, 0))
        self.healra = Skill("Healra",  "Heal self for 125 health", 125, 0, "Single", 45,
                            "Magical", "Healing", (0, 0, 0))
        # Buff & Healing Skills END

        # Unique Monster Skills
        self.wingSweep = Skill("Wing Sweep",  "Attack an enemy. Unique to Bat", 13, 5, "Single", 0,
                               "Strike", "Physical", (0, 0, 0))
        self.slimeBounce = Skill("Slime Smash",  "Attack an enemy. Unique to Slime", 12, 2, "Single", 0,
                                 "Strike", "Physical", (0, 0, 0))
        self.drainingBite = Skill("Draining Bite",  "Steals mana from enemy. Unique to spider.", 20, 5, "Single", 0,
                                  "Strike", "Drain", (0, 0, 0))
        self.lifeBite = Skill("Life Bite",  "Steals health from enemy. Unique to spider.", 15, 5, "Single", 0,
                              "Strike", "Drain", (0, 0, 0))
        self.cleanse = Skill("Cleanse", "Removes any status ailments on the user.", 7.5, 2.5, "Single",
                             15, 'Light', "Cleanse", (250, 187, 0))
        self.poison = Skill("Poison", "Poisons an enemy", 4, 0, "Single",
                            8, 'Poison', "Ailment", (235, 234, 176))
        self.silence = Skill("Silence", "Silences an enemy", 4, 0, "Single",
                             8, 'Silence', "Ailment", (235, 234, 176))
        self.blind = Skill("Blind", "Blinds an enemy", 4, 0, "Single",
                           8, "Blind", "Ailment", (235, 234, 176))
        # Unique Monster Skills END


class Equips:
    def __init__(self):
        # Weapon (Name, Speed, Attack, Magic, Crit Rate, Element, Scope)
        # Armor (Name, Speed, Health, physical defense, magical defense, luck, elemental resist)
        self.scythe = Weapon("Flaming Scythe", 0, 3, 3, 0.05, 'Fire',
                             "Multiple")
        # REMEMBER THAT EACH OF THESE VARIABLES ARE NOTTT GLOBAL
        self.silverSword = Weapon("Silver Sword", 2, 4, 0, 0.03,
                                  'Strike', "Single")
        self.woodenStaff = Weapon("Wooden Staff", 0, 1, 6, 0.01,
                                  'Strike', "Single")
        self.bow = Weapon("Bow", 3, 1, 1, 0.08,
                          'Strike', "Single")
        self.filler = Weapon("Blank", 5, 1, 0, 0.03,
                             'Strike', "Single")
        self.plating = Armor("Plating", 1, 15, 3, 1, 0, {
            'Fire': 1, 'Water': 1, 'Electric': 1, 'Ice': 1, 'Dark': 1, 'Light': 1, 'Strike': 1})
        self.robe = Armor("Robe", 3, 5, 1, 3, 2, {
            'Fire': 1, 'Water': 1, 'Electric': 1, 'Ice': 1, 'Dark': 1, 'Light': 1, 'Strike': 1})

# enemy parameters: (health, skillDictionary, name, goldReward, experienceReward, speed,
# attackDamage, magicDamage,
# physicalDefense, magicDefense, elementalResistances, critRate, originalName):


class Enemies(Skills):
    def __init__(self):
        Skills.__init__(self)
        self.elementResistance = {'Fire': 1, 'Water': 1, 'Electric': 2,
                                  'Ice': 0, 'Dark': 1.5, 'Light': 1, 'Strike': 1}
        self.elementResistance2 = {'Fire': 1, 'Water': 1, 'Electric': 1,
                                   'Ice': 1.5, 'Dark': 0.5, 'Light': 1, 'Strike': 1}
        self.slimeEnemy = Enemy(85, {self.silence: 40, self.slimeBounce: 60, self.zap: 100},
                                'Slime', 10, 15, 5, 20, 20, 2, 4, self.elementResistance, 0.05, 'Slime')
        self.skeletonEnemy = Enemy(75, {self.darkStrike: 40, self.telekinesis: 100},
                                   'Skull', 10, 15, 3, 15, 28, 12, 4, {'Fire': 1, 'Water': 1, 'Electric': 1,
                                                                       'Ice': 1.7, 'Dark': 1, 'Light': 0, 'Strike': 1}, 0.05, 'Skull')
        self.batEnemy = Enemy(52, {self.wingSweep: 50, self.poison: 100}, 'Bat',
                              10, 15, 15, 15, 15, 3, 3, self.elementResistance2, 0.15, 'Bat')
        self.ghostEnemy = Enemy(60, {self.blind: 40, self.darkStrike: 75, self.fireballSpell: 100}, 'Ghost', 10, 20, 8, 2, 25, 3, 6, {'Fire': 1, 'Water': 1, 'Electric': 1,
                                                                                                                                      'Ice': 1, 'Dark': 0, 'Light': 2, 'Strike': 0}, 0.10, 'Ghost')
        self.spiderEnemy = Enemy(45, {self.blind: 30, self.lifeBite: 60, self.drainingBite: 100}, 'Spider', 10, 15, 12, 3, 3, 6, 3, {'Fire': 1, 'Water': 1.5, 'Electric': 0.5,
                                                                                                                                     'Ice': 1, 'Dark': 1, 'Light': 1, 'Strike': 1}, 0.15, 'Spider')

        self.wolfEnemy = Enemy(70, {self.bluntStrike: 100}, 'Wolf', 10, 25, 23, 11, 1, 9, 3, {'Fire': 1.5, 'Water': 1, 'Electric': 1,
                                                                                              'Ice': 1, 'Dark': 1.5, 'Light': 1, 'Strike': 1}, 0.30, 'Wolf')

        self.unicornEnemy = Enemy(75, {self.holy: 60, self.heal: 100}, 'Unicorn', 10, 20, 13, 1, 20, 1, 4, {'Fire': 1.6, 'Water': 1, 'Electric': 1,
                                                                                                            'Ice': 1, 'Dark': 1, 'Light': 0.5, 'Strike': 2.0}, 0.15, 'unicorn')


class Classes(Skills, Equips):
    def __init__(self):
        Skills.__init__(self)
        Equips.__init__(self)
        # Player: atkDMG, magDMG, phyDEF, magDEF, luck, speed, Energy, CurrEnergy, Health, CurrHealth, gold, experience, level, weapon, armor, skills, elementalResistances
        self.baseElementalResist = {'Fire': 1, 'Water': 1, 'Electric': 1,
                                    'Ice': 1.5, 'Dark': 1, 'Light': 1, 'Strike': 1}
        self.wizard = Player(3, 12, 4, 8, 2, 4, 230, 230, 240, 240, 500, 0,
                             1, self.woodenStaff, self.robe, [self.fireballSpell,
                                                              self.freezeSpell, self.water, self.zap], self.baseElementalResist)
        self.warrior = Player(8, 3, 10, 7, 5, 9, 130, 130, 350, 350, 500, 0,
                              1, self.silverSword, self.plating, [self.bluntStrike,
                                                                  self.electricSlash, self.charge, self.heal], self.baseElementalResist)
        self.archer = Player(7, 5, 7, 7, 10, 14, 150, 150, 280, 280, 500, 0,
                             1, self.bow, self.plating, [self.heal,
                                                         self.fireballSpell, self.darkStrike, self.freezeSpell], self.baseElementalResist)
        self.cleric = Player(6, 9, 5, 10, 5, 7, 200, 200, 350, 350, 500, 0,
                             1, self.silverSword, self.plating, [self.heal,
                                                                 self.holy, self.darkStrike, self.cleanse], self.baseElementalResist)
        self.listClasses = [
            self.wizard, self.warrior, self.archer, self.cleric]
