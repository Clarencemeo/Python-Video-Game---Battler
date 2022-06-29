from BattlePrep.abilities import *
from BattlePrep.equipment import *
import globalVariables


def init():
    # Below are the initializations for the skills, weapons, and armor.
    # Skill(Name, base dmg, var dmg, scope, energy cost, element, skillType)
    fireballSpell = Skill("Fireball", 7.5, 2.5, "Single", 8, 'Fire', "Magical")
    darkStrike = Skill("Dark Strike", 7.5, 2.5, "Single", 8, 'Dark', "Magical")
    freezeSpell = Skill("Freezing Bolt", 7.5, 2.5,
                        "Single", 8, 'Ice', "Magical")
    motivate = BuffDebuffSkill("Motivate", 5, "Attack Damage", 5, "Buff")
    zap = Skill("Zap", 7.5, 2.5, "Single", 8, "Electric", "Magical")
    basicAttack = Skill("Attack", 3, 1, "Single", 0, "Fire", "Physical")
    globalVariables.everySkill = [basicAttack,
                                  fireballSpell, freezeSpell, motivate, zap]

    # Weapon (Name, Speed, Attack, Magic, Crit Rate, Element, Scope)
    # Armor (Name, Speed, Health, physical defense, magical defense, luck, elemental resist)
    scythe = Weapon("Flaming Scythe", 0, 3, 3, 0.05, 'Fire', "Multiple")
    silverSword = Weapon("Silver Sword", 5, 1, 0, 0.03, 'Physical', "Single")
    plating = Armor("Plating", 2, 15, 1, 1, 1, {
                    'Fire': 3, 'Water': 2, 'Electric': 0, 'Ice': 5, 'Dark': 3, 'Light': -1, 'Physical': 0})
    globalVariables.everyWeapon = [scythe, silverSword]
    globalVariables.everyArmor = [plating]
