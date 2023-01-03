from gameFunc import mainGame
import initializations.globalVariables
import initializations.skillsEquipment
globalVarPath = initializations.globalVariables
globalVarPath.init()
skillsEquipmentPath = initializations.skillsEquipment
skillsEquipmentPath. init()
g = mainGame()

while g.running:
    g.curr_menu.display_menu()
