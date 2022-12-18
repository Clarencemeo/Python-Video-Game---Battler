import pygame
from BattlePrep.equipment import Armor, Weapon
import BattlePrep.inventorySlot

# each weapon and armor can have their own image in their own class
# as for the positions,

# each weapon, armor, and item will also have their own description for when you click on them.


class Inventory:
    def __init__(self, maxCapacity):
        # initialize bag slot to have 36 spots
        self.slots = [0] * 36
        # tracks which slot we are currently replacing.
        self.slotCounter = 0
        # self.image is going to be the grid inventory
        self.image = pygame.image.load("Assets/inventoryGrid.png")
        #self.slot = InventorySlot("Images")
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        # Note that these coordinates are for the image display, not the cursor!
        self.currentXCoordinate = 30
        self.currentYCoordinate = 30
        self.maxCapacity = maxCapacity
        #self.slots.append(InventorySlot("Assets/SilverSword.png"), (10, 350))

    def render(self, display):
        # draw the actual inventory background
        display.blit(self.image, self.rect)
        # draw each inventory slot
        # for each item in slots, draw each individual one by calling render
        for slot in self.slots:
            #include or item
            # this ensures that the empty slots dont generate an error (because integers do not have render functions)
            if isinstance(slot, BattlePrep.inventorySlot.InventorySlot):
                slot.render(display)

    # can be either a weapon or a piece of armor or items
    # remember to check if slotCounter is below 36 to ensure inventory is not full
    def addToInventory(self, equipment):
        if self.slotCounter < 36:
            # the self.currentXCoordinate and self.currentYCoordinate record which grid the item should go in
            self.slots[self.slotCounter] = BattlePrep.inventorySlot.InventorySlot(
                equipment, (self.currentXCoordinate, self.currentYCoordinate))
            self.slotCounter += 1
            # : we can probably keep this here... but what about when we move down?
            self.currentXCoordinate += 30
            # to change currentYCoordinate. this means we are at end of row and we click right.
            if self.slotCounter >= 9:
                pass
        # conflicted about how to manage the positions.
