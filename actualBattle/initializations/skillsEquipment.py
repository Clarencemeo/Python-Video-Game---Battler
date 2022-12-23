from BattlePrep.abilities import *
from BattlePrep.equipment import *
import initializations.globalVariables

# silverSword = Weapon("Silver Sword", 5, 1, 0, 0.03,
#                     'Physical', "Single", "Assets/SilverSword.png")


def init():
    # Below are the initializations for the skills, weapons, and armor.
    # Skill(Name, base dmg, var dmg, scope, energy cost, element, skillType)
    fireballSpell = Skill("Fireball", 7.5, 2.5, "Single",
                          8, 'Fire', "Magical", (245, 72, 66))
    darkStrike = Skill("Dark", 7.5, 2.5, "Single",
                       8, 'Dark', "Magical", (97, 88, 87))
    freezeSpell = Skill("Ice", 7.5, 2.5,
                        "Single", 8, 'Ice', "Magical", (17, 250, 246))
    motivate = BuffDebuffSkill(
        "Motivate", 5, "Attack Damage", 5, "Buff", (203, 209, 209))
    zap = Skill("Zap", 7.5, 2.5, "Single", 8,
                "Electric", "Magical", (235, 231, 26))
    basicAttack = Skill("Attack", 6, 1, "Single", 0,
                        "Physical", "Physical", (0, 0, 0))
    initializations.globalVariables.everySkill = [basicAttack,
                                                  fireballSpell, darkStrike, freezeSpell, motivate, zap]
    initializations.globalVariables.equippedSkills = [fireballSpell,
                                                      freezeSpell, darkStrike, zap]

    # Weapon (Name, Speed, Attack, Magic, Crit Rate, Element, Scope)
    # Armor (Name, Speed, Health, physical defense, magical defense, luck, elemental resist)
    scythe = Weapon("Flaming Scythe", 0, 3, 3, 0.05, 'Fire',
                    "Multiple", "Assets/FlamingScythe.png")
    # REMEMBER THAT EACH OF THESE VARIABLES ARE NOTTT GLOBAL
    global silverSword
    silverSword = Weapon("Silver Sword", 5, 1, 0, 0.03,
                         'Physical', "Single", "Assets/silverSword.png")
    filler = Weapon("Blank", 5, 1, 0, 0.03,
                    'Physical', "Single", "Assets/silverSword.png")
    plating = Armor("Plating", 2, 15, 1, 1, 1, {
                    'Fire': 3, 'Water': 2, 'Electric': 0, 'Ice': 5, 'Dark': 3, 'Light': -1, 'Physical': 0})
    initializations.globalVariables.everyWeapon = [scythe, silverSword]
    initializations.globalVariables.everyArmor = [plating]
# enemy parameters: (health, skillDictionary, dropsDictionary, name, goldReward, experienceReward, speed,
#attackDamage, magicDamage,
# physicalDefense, magicDefense, elementalResistances):
    elementResistance = {'Fire': 3, 'Water': 2, 'Electric': 0,
                         'Ice': 10, 'Dark': -10, 'Light': -1, 'Physical': 0}
    elementResistance2 = {'Fire': 7, 'Water': 2, 'Electric': 0,
                          'Ice': -3, 'Dark': 10, 'Light': -1, 'Physical': 0}
    slimeEnemy = Enemy(50, {freezeSpell: 75, zap: 100}, {
                       plating: 0.25}, 'Slime', 10, 15, 5, 20, 20, 2, 4, elementResistance, 0.05)
    batEnemy = Enemy(25, {darkStrike: 75, fireballSpell: 100}, {
                     plating: 0.25}, 'Bat', 10, 15, 15, 15, 15, 3, 3, elementResistance2, 0.05)
    initializations.globalVariables.monsterList1 = [slimeEnemy, batEnemy]

    initializations.globalVariables.protagonist = Player(200, 200, 500, 500, 500, 0,
                                                         1, scythe, plating, [fireballSpell], {'Fire': 3, 'Water': 2, 'Electric': 0, 'Ice': 5, 'Dark': 3, 'Light': -1, 'Physical': 0})
