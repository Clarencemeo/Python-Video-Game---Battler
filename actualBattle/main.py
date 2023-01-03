from gameFunc import mainGame
from initializations.skillsEquipment import Skills
import initializations.skillsEquipment
skillsEquipmentPath = initializations.skillsEquipment
#skillsEquipmentPath. init()

g = mainGame()

while g.running:
    g.curr_menu.display_menu()
