import time
from IPython.display import clear_output
from Fighters.player import Player
import json
import initializations.globalVariables
globalVarPath = initializations.globalVariables
######################################################################
#
# All code in this section is for the preparation screen, where
# the player can equip skills, armor, weapons, etc.
#
######################################################################


def preparationScreen():
    # the code below is used for the preparation screen
    # in which the user can choose which armor, weapons, and skills to equip.
    keepEquipping = True
    while (keepEquipping):
        firstEquipPrompt = input(
            "What would you like to equip?\nType in 'weapons', 'armor', 'skills' to equip those respectively.\nYou may also type in 'cancel' to stop equipping.")
        if (firstEquipPrompt.upper() == "CANCEL"):
            keepEquipping = False

        if (firstEquipPrompt.upper() == "ARMOR"):
            #
            # CODE BELOW FOR EQUIPPING ARMOR
            #
            clear_output()
            keepArmoring = True
            while (keepArmoring):
                invalidEquipArmor = False
                print("You currently have " +
                      globalVarPath.protagonist.getArmor().getName() + " equipped.")
                armorInput = input(
                    "Which armor would you like to equip?\nType in 'inventory' to see all the armor you have.\nType in 'cancel' to stop equipping weapons.")

                if (armorInput.upper() == "INVENTORY"):
                    clear_output()
                    print("Here are the armor in your inventory:")
                    for armor in globalVarPath.armorInventory:
                        print(armor.getName())
                        invalidEquipArmor = True

                if (armorInput.upper() == "CANCEL"):
                    clear_output()
                    keepArmoring = False
                    invalidEquipArmor = True

                if (globalVarPath.protagonist.getArmor().getName().upper() == armorInput.upper()):
                    clear_output()
                    print("You already have that armor equipped.\n")
                    invalidEquipArmor = True

                if (invalidEquipArmor == False):
                    for armor in globalVarPath.armorInventory:
                        if (armor.getName().upper() == armorInput.upper()):
                            globalVarPath.protagonist.changeArmor(armor)
                            clear_output()
                            print("Successfully equipped " +
                                  globalVarPath.protagonist.getArmor().getName() + "!")
                            keepArmoring = False
                    if (keepArmoring):
                        clear_output()
                        print("Invalid selection.\n")

            with open('saveData.json', 'w') as outfile:
                globalVarPath.allSaveData["currentArmorEquip"] = globalVarPath.protagonist.getArmor(
                ).getName()
                json.dump(globalVarPath.allSaveData, outfile)
            #
            # CODE FOR EQUIPPING ARMOR ENDS HERE
            #

        if (firstEquipPrompt.upper() == "WEAPONS"):
            #
            # CODE BELOW FOR EQUIPPING WEAPONS
            #
            clear_output()
            keepWeaponing = True
            while (keepWeaponing):
                invalidEquipWeapon = False
                print("You currently have " +
                      globalVarPath.protagonist.getWeapon().getName() + " equipped.")
                weaponInput = input(
                    "Which weapon would you like to equip?\nType in 'inventory' to see all the weapons you have.\nType in 'cancel' to stop equipping weapons.")

                if (weaponInput.upper() == "INVENTORY"):
                    clear_output()
                    print("Here are the weapons in your inventory:")
                    for weapon in globalVarPath.weaponInventory:
                        print(weapon.getName())
                        invalidEquipWeapon = True

                if (weaponInput.upper() == "CANCEL"):
                    clear_output()
                    keepWeaponing = False
                    invalidEquipWeapon = True

                if (globalVarPath.protagonist.getWeapon().getName().upper() == weaponInput.upper()):
                    clear_output()
                    print("You already have that weapon equipped.\n")
                    invalidEquipWeapon = True

                if (invalidEquipWeapon == False):
                    for weapon in globalVarPath.weaponInventory:
                        if (weapon.getName().upper() == weaponInput.upper()):
                            globalVarPath.protagonist.changeWeapon(weapon)
                            clear_output()
                            print("Successfully equipped " +
                                  globalVarPath.protagonist.getWeapon().getName() + "!")
                            keepWeaponing = False
                    if (keepWeaponing):
                        clear_output()
                        print("Invalid selection.\n")

            with open('saveData.json', 'w') as outfile:
                globalVarPath.allSaveData["currentWeaponEquip"] = globalVarPath.protagonist.getWeapon(
                ).getName()
                json.dump(globalVarPath.allSaveData, outfile)
            #
            # CODE FOR EQUIPPING WEAPONS ENDS HERE
            #
        if (firstEquipPrompt.upper() == "SKILLS"):
            #
            # CODE BELOW FOR EQUIPPING SKILLS
            #
            clear_output()
            keepPrompting = True
            while(keepPrompting):  # keep asking the user to equip a skill until its valid
                # otherOptions will track if the user picks one of the other options (i.e if they choose to view equips or unlocks instead)
                # checkInvalidSkill will check if the user enters in a valid skill input
                # continueEquipping will be used later to track if the user can keep equipping skills
                otherOptions = False
                checkInvalidSkill = True
                continueEquipping = True
                userInput = input(
                    "Which skill would you like to equip?\nType in 'equips' to see what you currently have equipped and 'unlocks' to see all the skills you have unlocked.\nYou can also type in 'cancel' to stop equipping skills.")
                clear_output()
                if (userInput.upper() == "EQUIPS"):
                    print("Here are the skills you currently have equipped:\n")
                    printList(globalVarPath.equippedSkills_string)
                    otherOptions = True
                if (userInput.upper() == "UNLOCKS"):
                    print("Here are the skills you currently have unlocked:\n")
                    for item in globalVarPath.unlockedSkills_string:
                        printEquipped = False
                        for skill in globalVarPath.equippedSkills_string:
                            if (item == skill):
                                printEquipped = True
                        if (printEquipped):
                            print(item + " (Equipped)")
                        else:
                            print(item)
                    otherOptions = True
                if (userInput.upper() == "CANCEL"):
                    keepPrompting = False
                    checkInvalidSkill = False
                if (otherOptions == False):
                    # this for loop checks if the skill input the user submitted is an unlocked skill
                    for skill_string in globalVarPath.unlockedSkills_string:
                        if (userInput.upper() == skill_string.upper()):
                            # this for loop makes sure the skill the user inputted is not CURRENTLY equippedt
                            for skillsEquipped in globalVarPath.equippedSkills_string:
                                if (userInput.upper() == skillsEquipped.upper()):
                                    print("You already have " +
                                          userInput + " equipped!")
                                    continueEquipping = False
                            # If the skill is not already equipped, then proceed with the equip process
                            if (continueEquipping):
                                clear_output()
                                print(
                                    "Here are the skills you currently have equipped:\n")
                                # print every skill you have equipped currently
                                printList(
                                    globalVarPath.equippedSkills_string)
                                replaceInput = input("Which skill would you like to replace with " +
                                                     skill_string + "?\nYou can also type in 'none' to cancel this selection.\n")
                                if (replaceInput.upper() == "ATTACK"):
                                    clear_output()
                                    checkInvalidSkill = False
                                    print(
                                        "You can't replace your default attack.")
                                    time.sleep(3)
                                    clear_output()
                                elif (replaceInput.upper() == 'NONE'):
                                    checkInvalidSkill = False
                                    clear_output()
                                else:
                                    # replace the skill at the index where we find it
                                    for index, skill3 in enumerate(globalVarPath.equippedSkills_string):
                                        if (skill3.upper() == replaceInput.upper()):
                                            globalVarPath.equippedSkills_string[index] = skill_string
                                            clear_output()
                                            print(
                                                userInput + " was successfully equipped!")
                                            checkInvalidSkill = False
                                            continueEquipping = input(
                                                "Would you like to continue equipping skills? Type in 'yes' to continue equipping skills.")
                                            if (continueEquipping.upper() == "YES"):
                                                keepPrompting = True
                                                clear_output()
                                            else:
                                                keepPrompting = False

                    if (checkInvalidSkill):
                        print(userInput + " is not a valid selection.")

            # equippedSkills is the same as equippedSkills_string,
            # except the strings are turned into their Skill representations

            for eachSkill in globalVarPath.equippedSkills_string:
                # for every string representation of a skill in the equippedSkills_string list,
                # find the corresponding skill from the everySkill list and add it to equippedSkills
                findSkill(eachSkill, globalVarPath.equippedSkills)
            with open('saveData.json', 'w') as outfile:
                globalVarPath.allSaveData["equippedSkills"] = globalVarPath.equippedSkills_string
                json.dump(globalVarPath.allSaveData, outfile)
            #
            # Code for equipping skills ends here
            #
    ######################################################################
    #
    # Code for the preparation screen ends here
    # NOTE: The dumping into the JSON could and should be moved off the if statements
    ######################################################################

    # should track progress on a stage by stage basis
    # and save data after every stage
    # maybe include a retry option at the end of every stage
    # that just loads the save data
