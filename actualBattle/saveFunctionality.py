# update game to be synchronized with save
import initializations.globalVariables
import initializations.skillsEquipment
import json
globalVarPath = initializations.globalVariables
skillsEquipmentPath = initializations.skillsEquipment


def findSkill(specificSkillName, skillList):
    for skill in skillsEquipmentPath.everySkill:
        if (skill.getName() == specificSkillName):
            skillList.append(skill)


def findWeapon(specificWeaponName, weaponList):
    for weapon in skillsEquipmentPath.everyWeapon:
        if (weapon.getName() == specificWeaponName):
            weaponList.append(weapon)


def findArmor(specificArmorName, armorList):
    for armor in skillsEquipmentPath.everyArmor:
        if (armor.getName() == specificArmorName):
            armorList.append(armor)


def resetSaveData():
    with open('unlockables.json', 'w') as json_file:
        unlockData = {"skillUnlocks": ["Attack", "Fireball", "Freezing Bolt", "Motivate", "Zap"], "weaponUnlocks": [
            "Scythe", "Silver Sword"], "armorUnlocks": ["Plating"], "varietyPaths": ["merchant", "ambush", "campfire"]}
        json.dump(unlockData, json_file)
    with open('saveData.json', 'w') as json_file:
        saveData = {}
        saveData["equippedSkills"] = [
            "Fireball", "Zap", "Freezing Bolt", "Motivate"]
        saveData["weaponInventory"] = ["Scythe", "Silver Sword"]
        saveData["armorInventory"] = ["Plating"]
        saveData["currentArmorEquip"] = "Plating"
        saveData["currentWeaponEquip"] = "Silver Sword"
        saveData["level"] = 1
        saveData["experience"] = 0
        saveData["health"] = 500
        saveData["currHealth"] = 500
        saveData["energy"] = 300
        saveData["gold"] = 100
        saveData["stage"] = 1
        saveData["node"] = 1
        json.dump(saveData, json_file)


def synchronizeSave():
    # read through the json file and keep track
    # of all the skills that are unlocked.
    with open('unlockables.json') as json_file:
        data = json.load(json_file)
    # read in the unlockables and store them in this list that
    # can be accessed everywhere
    globalVarPath.allUnlocksFromJson = data
    # unlockedSkills_string would return a list of skills in their string representation
    unlockedSkills_string = globalVarPath.allUnlocksFromJson["skillUnlocks"]
    unlockedWeapons_string = globalVarPath.allUnlocksFromJson["weaponUnlocks"]
    unlockedArmors_string = globalVarPath.allUnlocksFromJson["armorUnlocks"]
    varietyPathUnlocks = globalVarPath.allUnlocksFromJson["varietyPaths"]
    # opens up saveData which has level, skills equipped, etc.
    with open('saveData.json') as json_file:
        data = json.load(json_file)
    globalVarPath.allSaveData = data
    ourStage = globalVarPath.allSaveData["stage"]
    ourNode = globalVarPath.allSaveData["node"]
    # the next few lines equip the skills that were listed as
    # equipped by the save file.

    equippedSkills_string = globalVarPath.allSaveData["equippedSkills"]
    for eachSkill in equippedSkills_string:
        # for every string representation of a skill in the equippedSkills_string list,
        # find the corresponding skill from the everySkill list and add it to equippedSkills
        findSkill(eachSkill,  globalVarPath.equippedSkills)
    # equips the current weapon from the save file
    for weapon in skillsEquipmentPath.everyWeapon:
        if (weapon.getName().upper() == globalVarPath.allSaveData["currentWeaponEquip"].upper()):
            currentWeapon = weapon
    # equips the current armor from the save file
    for armor in skillsEquipmentPath.everyArmor:
        if (armor.getName().upper() == globalVarPath.allSaveData["currentArmorEquip"].upper()):
            currentArmor = armor
    # synchronize the inventories
    weaponInventory = []
    armorInventory = []
    for weapon in globalVarPath.allSaveData["weaponInventory"]:
        findWeapon(weapon, weaponInventory)
    for armor in globalVarPath.allSaveData["armorInventory"]:
        findArmor(armor, armorInventory)
