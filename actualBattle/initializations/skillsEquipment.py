from BattlePrep.abilities import *
from BattlePrep.equipment import *
import initializations.globalVariables

# silverSword = Weapon("Silver Sword", 5, 1, 0, 0.03,
#                     'Physical', "Single", "Assets/SilverSword.png")


def init():
    # Below are the initializations for the skills, weapons, and armor.
    # Skill(Name, description, base dmg, var dmg, scope, energy cost, element, skillType, color)
    fireballSpell = Skill("Fireball", "Deals low magical fire damage to one enemy.", 7.5, 2.5, "Single",
                          8, 'Fire', "Magical", (245, 72, 66))
    water = Skill("Torrent", "Deals low magical water damage to one enemy.", 7.5, 2.5, "Single",
                  8, 'Water', "Magical", (0, 92, 250))
    darkStrike = Skill("Dark",  "Deals low magical dark damage to one enemy.", 7.5, 2.5, "Single",
                       8, 'Dark', "Magical", (97, 88, 87))
    freezeSpell = Skill("Ice",  "Deals low magical ice damage to one enemy.", 7.5, 2.5,
                        "Single", 8, 'Ice', "Magical", (17, 250, 246))
    charge = Skill("Charge",  "Your next attack deals 2.5x more damage.", 7.5, 2.5,
                   "Single", 13, 'Charged', "Buff", (235, 234, 176))
    zap = Skill("Zap",  "Deals low magical electric damage to one enemy.", 7.5, 2.5, "Single", 8,
                "Electric", "Magical", (235, 231, 26))
    global basicAttack
    basicAttack = Skill("Attack",  "Attack an enemy. Effects differ based on weapon.", 6, 1, "Single", 0,
                        "Strike", "Physical", (0, 0, 0))
    electricSlash = Skill("ESlash",  "Deal low physical electric damage to one enemy.", 9, 3, "Single", 10,
                          "Electric", "Physical", (235, 231, 26))
    bluntStrike = Skill("Skewer",  "Deal moderate physical strike damage to one enemy.", 16, 5, "Single", 15,
                        "Strike", "Physical", (0, 0, 0))
    heal = Skill("Heal",  "Heal self for 50 health", 6, 1, "Single", 35,
                 "Magical", "Healing", (0, 0, 0))
    wingSweep = Skill("Wing Sweep",  "Attack an enemy. Unique to Bat", 13, 5, "Single", 0,
                      "Strike", "Physical", (0, 0, 0))
    slimeBounce = Skill("Slime Smash",  "Attack an enemy. Unique to Slime", 12, 2, "Single", 0,
                        "Strike", "Physical", (0, 0, 0))
    drainingBite = Skill("Draining Bite",  "Steals mana from enemy. Unique to spider.", 20, 5, "Single", 0,
                         "Strike", "Drain", (0, 0, 0))
    lifeBite = Skill("Life Bite",  "Steals health from enemy. Unique to spider.", 15, 5, "Single", 0,
                     "Strike", "Drain", (0, 0, 0))
    holy = Skill("Holy", "Deals low magical light damage to one enemy.", 7.5, 2.5, "Single",
                 8, 'Light', "Magical", (235, 234, 176))
    cleanse = Skill("Cleanse", "Removes any status ailments on the user.", 7.5, 2.5, "Single",
                    15, 'Light', "Cleanse", (250, 187, 0))
    poison = Skill("Poison", "Poisons an enemy", 4, 0, "Single",
                   8, 'Poison', "Ailment", (235, 234, 176))
    silence = Skill("Silence", "Silences an enemy", 4, 0, "Single",
                    8, 'Silence', "Ailment", (235, 234, 176))
    blind = Skill("Blind", "Blinds an enemy", 4, 0, "Single",
                  8, "Blind", "Ailment", (235, 234, 176))
    # Weapon (Name, Speed, Attack, Magic, Crit Rate, Element, Scope)
    # Armor (Name, Speed, Health, physical defense, magical defense, luck, elemental resist)
    scythe = Weapon("Flaming Scythe", 0, 3, 3, 0.05, 'Fire',
                    "Multiple")
    # REMEMBER THAT EACH OF THESE VARIABLES ARE NOTTT GLOBAL
    global silverSword
    silverSword = Weapon("Silver Sword", 2, 4, 0, 0.03,
                         'Strike', "Single")
    woodenStaff = Weapon("Wooden Staff", 0, 1, 6, 0.01,
                         'Strike', "Single")
    bow = Weapon("Bow", 3, 1, 1, 0.08,
                 'Strike', "Single")
    filler = Weapon("Blank", 5, 1, 0, 0.03,
                    'Strike', "Single")
    plating = Armor("Plating", 1, 15, 3, 1, 0, {
                    'Fire': 1, 'Water': 1, 'Electric': 1, 'Ice': 1, 'Dark': 1, 'Light': 1, 'Strike': 1})
    robe = Armor("Robe", 3, 5, 1, 3, 2, {
        'Fire': 1, 'Water': 1, 'Electric': 1, 'Ice': 1, 'Dark': 1, 'Light': 1, 'Strike': 1})
    initializations.globalVariables.everyWeapon = [scythe, silverSword]
    initializations.globalVariables.everyArmor = [plating]


# enemy parameters: (health, skillDictionary, dropsDictionary, name, goldReward, experienceReward, speed,
# attackDamage, magicDamage,
# physicalDefense, magicDefense, elementalResistances, critRate, originalName):

    elementResistance = {'Fire': 1, 'Water': 1, 'Electric': 2,
                         'Ice': 1, 'Dark': 1.5, 'Light': 1, 'Strike': 1}
    elementResistance2 = {'Fire': 1, 'Water': 1, 'Electric': 1,
                          'Ice': 1.5, 'Dark': 0.5, 'Light': 1, 'Strike': 1}
    slimeEnemy = Enemy(85, {silence: 40, slimeBounce: 60, zap: 100}, {
        plating: 0.25}, 'Slime', 10, 15, 5, 20, 20, 2, 4, elementResistance, 0.05, 'Slime')
    batEnemy = Enemy(45, {wingSweep: 50, poison: 100}, {
        plating: 0.25}, 'Bat', 10, 15, 15, 15, 15, 3, 3, elementResistance2, 0.15, 'Bat')
    ghostEnemy = Enemy(60, {blind: 40, darkStrike: 75, fireballSpell: 100}, {
        plating: 0.25}, 'Ghost', 10, 20, 8, 2, 25, 3, 6, {'Fire': 1, 'Water': 1, 'Electric': 1,
                                                          'Ice': 1, 'Dark': 0, 'Light': 2, 'Strike': 0}, 0.10, 'Ghost')
    spiderEnemy = Enemy(45, {blind: 30, lifeBite: 60, drainingBite: 100}, {
        plating: 0.25}, 'Spider', 10, 15, 12, 3, 3, 6, 3, {'Fire': 1, 'Water': 1.8, 'Electric': 0.5,
                                                           'Ice': 1, 'Dark': 1, 'Light': 1, 'Strike': 1}, 0.15, 'Spider')

    wolfEnemy = Enemy(70, {bluntStrike: 100}, {
        plating: 0.25}, 'Wolf', 10, 25, 23, 11, 1, 9, 3, {'Fire': 1.5, 'Water': 1, 'Electric': 1,
                                                          'Ice': 1, 'Dark': 1.5, 'Light': 1, 'Strike': 1}, 0.30, 'Wolf')

    unicornEnemy = Enemy(75, {holy: 60, heal: 100}, {
        plating: 0.25}, 'Unicorn', 10, 20, 13, 1, 20, 1, 4, {'Fire': 1.6, 'Water': 1, 'Electric': 1,
                                                             'Ice': 1, 'Dark': 1, 'Light': 0.5, 'Strike': 2.0}, 0.15, 'unicorn')
    initializations.globalVariables.monsterList1 = {
        "Slime": slimeEnemy, "Bat": batEnemy, "Ghost": ghostEnemy, "Spider": spiderEnemy, "Unicorn": unicornEnemy, "Wolf": wolfEnemy}

# Player: atkDMG, magDMG, phyDEF, magDEF, luck, speed, Energy, CurrEnergy, Health, CurrHealth, gold, experience, level, weapon, armor, skills, elementalResistances
    baseElementalResist = {'Fire': 1, 'Water': 1, 'Electric': 1,
                           'Ice': 1.5, 'Dark': 1, 'Light': 1, 'Strike': 1}
    wizard = Player(3, 12, 4, 8, 2, 4, 230, 230, 240, 240, 500, 0,
                    1, woodenStaff, robe, [fireballSpell,
                                           freezeSpell, water, zap], baseElementalResist)
    warrior = Player(8, 3, 10, 7, 5, 9, 130, 130, 350, 350, 500, 0,
                     1, silverSword, plating, [bluntStrike,
                                               electricSlash, charge, heal], baseElementalResist)
    archer = Player(7, 5, 7, 7, 10, 14, 150, 150, 280, 280, 500, 0,
                    1, bow, plating, [heal,
                                      fireballSpell, darkStrike, freezeSpell], baseElementalResist)
    cleric = Player(6, 9, 5, 10, 5, 7, 200, 200, 350, 350, 500, 0,
                    1, silverSword, plating, [heal,
                                              holy, darkStrike, cleanse], baseElementalResist)
    initializations.globalVariables.classList = [
        wizard, warrior, archer, cleric]
