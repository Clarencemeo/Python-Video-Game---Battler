import pygame
from inventorySlot import InventorySlot
# each weapon and armor can have their own image in their own class
# as for the positions,


class Inventory:
    def __init__(self):
        self.slots = []
        self.image = pygame.image.load("Assets/Inventory.png")
        self.slot = InventorySlot("Images")
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 350)
        #self.slots.append(InventorySlot("Assets/SilverSword.png"), (10, 350))

    def render(self, display):
        # draw the actual inventory background
        display.blit(self.image, self.rect)
        # draw each inventory slot
        # for each item in slots, draw each individual one by calling render
        for slot in self.slots:
            slot.render(display)

    # can be either a weapon or a piece of armor or items
    def addToInventory(self, equipment):
        self.slots.append(InventorySlot(equipment, (10, 350)))
