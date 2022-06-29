from gameFunc import mainGame
import initializations.globalVariables
import initializations.skillsEquipment
globalVarPath = initializations.globalVariables
globalVarPath.init()
skillsEquipmentPath = initializations.skillsEquipment
skillsEquipmentPath.init()
print(globalVarPath.everySkill)
g = mainGame()
while g.running:
    g.curr_menu.display_menu()
    g.game_loop()

    # forestMenu = pygame.transform.scale(pygame.image.load(
    #     os.path.join('Assets', 'mainMenu.jpg')), (self.game.WIDTH, self.game.HEIGHT))
