from gameFunc import mainGame

g = mainGame()

while g.running:
    g.curr_menu.display_menu()
