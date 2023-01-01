import copy
import time
import random
import initializations.globalVariables
globalVarPath = initializations.globalVariables
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


# finally got it working!
# ultimately chose a dictionary since it can
# track repeats for each individual enemy.

# this function is for when the player is using a skill in battle
# enemy troops should be a list of the enemies you're fighting
def userSkillBattle(enemyTroops):
    # make sure each enemy has a number just in case of dupes
    # while adding, check for dupes
    # clear_output()
    invalidSkill = True
    invalidEnemy = True
    while(invalidSkill & invalidEnemy):
        print("Your Health: " + str(globalVarPath.protagonist.getCurrHealth()) + " | Your Energy: " +
              str(globalVarPath.protagonist.getEnergy()) + " | Your Level: " + str(globalVarPath.protagonist.getLevel()))
        print("Here are the current enemies you are fighting:\n")
        for enemy in enemyTroops:
            print(enemy.getName() + " with " +
                  str(enemy.getHealth()) + " health.")
        print("\nHere are the skills you currently have equipped:\n")
        #print(basicAttack.getName() + " (Energy Cost: " + str(basicAttack.getEnergy()*-1) + ")"  )
        printSkills(globalVarPath.equippedSkills)
        chooseSkill = input("Which skill would you like to use?\n")
        if (chooseSkill.upper() == "SURRENDER"):
            invalidSkill = False
            invalidEnemy = False
        for eachSkill in globalVarPath.equippedSkills:
            if (chooseSkill.upper() == eachSkill.getName().upper()):
                invalidSkill = False
                # check if it's a buff/debuff skill and if so,
                # change it up.
                if (eachSkill.getScope() == "Single"):
                    if (globalVarPath.protagonist.getEnergy() < eachSkill.getEnergy()):
                        print("You do not have enough energy to use this skill!")
                    else:
                        clear_output()
                        print("Here are the current enemies you are fighting:\n")
                        for enemy in enemyTroops:
                            print(enemy.getName() + " with " +
                                  str(enemy.getHealth()) + " health.")
                        target = input("Which enemy would you like to target with " +
                                       eachSkill.getName() + "? Type 'back' to select skills again.")
                        clear_output()
                        if (target.upper() == "BACK"):
                            break
                        for enemy in enemyTroops:
                            if (target.upper() == enemy.getName().upper()):
                                eachSkill.executeSkill(
                                    enemy, globalVarPath.protagonist)
                                if (enemy.getHealth() <= 0):
                                    print("You defeated " +
                                          enemy.getName() + "!")
                                    enemyTroops.remove(enemy)
                                invalidEnemy = False
                        if (invalidEnemy == True):
                            clear_output()
                            print("Not a valid target.")
                elif (eachSkill.getScope() == "Multiple"):
                    clear_output()
                    for enemy in enemyTroops:
                        eachSkill.executeSkill(
                            enemy, globalVarPath.protagonist)
                        if (enemy.getHealth() <= 0):
                            print("You defeated " + enemy.getName() + "!")
                            enemyTroops.remove(enemy)
        if (invalidSkill):
            print(chooseSkill + " is not an unlocked skill you can use.")
            time.sleep(2)
            clear_output()
            time.sleep(0.5)


def enemyAction(specificEnemy):
    chosenSkill = specificEnemy.randomSkillSelection()
    result = chosenSkill.executeSkill(globalVarPath.protagonist, specificEnemy)
    return result

# call battleTime whenever you start a battle
# TODO: Implement drops from the enemy as well as updating the save file based on the users
# health and inventory.


def battleTime(monsters):
    # since stats will be changing throughout the way with buffs
    # and debuffs, let's record the initial values of each stat!
    totalGoldReward = 0
    totalExperienceReward = 0
    initialAttack = globalVarPath.protagonist.getAttackDamage()
    initialMagic = globalVarPath.protagonist.getMagicDamage()
    initialPhysdef = globalVarPath.protagonist.getPhysicalDefense()
    initialMagicdef = globalVarPath.protagonist.getMagicalDefense()
    # can add a check to see if buffed version of stats
    # is a percentage better than the initial stats
    # to see if the buff should be restricted.
    battleTroopers = assembleBattleTroop(monsters, 2)
    # below is for calculating rewards, since the original battleTroopers will be modified as enemies get defeated.
    tempBattleTroopers = assembleBattleTroop(monsters, 2)
    protagSpeed = globalVarPath.protagonist.getSpeed()
    globalVarPath.protagonist.resetTurnGauge()
    while(len(battleTroopers) > 0):
        # the turn gauge is adjusted based on the users speed.
        # The more speed the user has, the faster the turn gauge fills up,
        # which means the user can take more actions.
        globalVarPath.protagonist.changeTurnGauge(protagSpeed)
        if (globalVarPath.protagonist.getTurnGauge() >= 50):
            userSkillBattle(battleTroopers)
            globalVarPath.protagonist.resetTurnGauge()
            clear_output()
        for enemy in battleTroopers:
            enemy.changeTurnGauge(enemy.getSpeed())
            if (enemy.getTurnGauge() >= 50):
                enemyAction(enemy)
                enemy.resetTurnGauge()
                clear_output()
    # if protagonist wins
    print("You defeated every enemy!")
    time.sleep(0.5)
    for eachMonster in tempBattleTroopers:
        totalGoldReward += eachMonster.getGoldReward()
        totalExperienceReward += eachMonster.getExperienceReward()
    print("Gold gained: " + str(totalGoldReward))
    time.sleep(0.5)
    levelUpCalculation(globalVarPath.protagonist,
                       totalExperienceReward, 'saveData.json')
    time.sleep(0.5)
    with open('saveData.json', 'w') as outfile:
        globalVarPath.allSaveData["currHealth"] = globalVarPath.protagonist.getCurrHealth(
        )
        globalVarPath.allSaveData["energy"] = globalVarPath.protagonist.getEnergy(
        )
        json.dump(globalVarPath.allSaveData, outfile)
