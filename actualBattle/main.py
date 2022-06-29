from gameFunc import mainGame
import initializations.globalVariables
import initializations.skillsEquipment
globalVarPath = initializations.globalVariables
skillsEquipmentPath = initializations.skillsEquipment
globalVarPath.init()
skillsEquipmentPath.init()
print(globalVarPath.everySkill)
g = mainGame()
while g.running:
    g.curr_menu.display_menu()
    g.game_loop()
