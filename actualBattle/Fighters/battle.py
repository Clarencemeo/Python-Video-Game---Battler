import copy
import random
from Menus import setupMenus
# given a list of possible monsters, assemble
# a battle troop that the player will face.


def assembleBattleTroop(monsterList, count):
    battleTroopDictionary = {}
    # Create a dictionary based on the monsterList.
    # The keys will be the enemies from the monsterList,
    # and the values will end up being how many dupes of
    # that enemy are in each troop.
    battleTroopDictionary = dict.fromkeys(monsterList, 1)
    finalBattleTroop = []
    while (count > 0):
        randomEnemyIndex = random.randint(0, len(monsterList)-1)
        randomEnemy = monsterList[randomEnemyIndex]
        for enemy in finalBattleTroop:
            # check if the enemy being added is already in the troop.
            # if so, increase relevant value in dictionary
            if (enemy.getName() == randomEnemy.getName()):
                battleTroopDictionary[enemy] += 1
        if (battleTroopDictionary[randomEnemy] > 1):
            # deepcopy basically makes the dupe seperate from the original!
            dupe = copy.deepcopy(randomEnemy)
            dupe.modifyName(battleTroopDictionary[randomEnemy])
            finalBattleTroop.append(dupe)
        else:
            finalBattleTroop.append(randomEnemy)
        count -= 1
    return finalBattleTroop


def levelUpCalculation(theProtagonist, experiencePointsGained):
    # every level requires 25 more exp than the previous
    levelCap = theProtagonist.getLevel() * 25
    theProtagonist.adjustExperience(experiencePointsGained)
    if (theProtagonist.getExperience() >= levelCap):
        # leftOverExperience after leveling up
        leftoverExperience = theProtagonist.getExperience() - levelCap
        # reset experience after leveling up
        theProtagonist.setExperience(0)
        # add over the leftover experience
        theProtagonist.adjustExperience(leftoverExperience)
        theProtagonist.adjustLevel(1)
        # actually level up
        # bottom condtional statement just in case the leftOverExperience ended up resulting in another level up.
        return True
    elif (theProtagonist.getExperience() >= theProtagonist.getLevel() * 25):
        pass
    else:
        return False
