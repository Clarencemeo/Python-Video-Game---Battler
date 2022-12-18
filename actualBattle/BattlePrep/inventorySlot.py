import pygame

# bagItem could either be a weapon, armor, or item


class InventorySlot:
    # maybe we could not pass in pos and just increment it as we add slots?
    # note that pos is not used as of yet
    def __init__(self, bagItem, pos):
        # load image for the singular item
        self.image = pygame.image.load(bagItem.getImage())
        pygame.Surface.convert_alpha(self.image)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.count = 0
        self.font = pygame.font.Font("Assets/Frostbite.ttf", 25)

    def render(self, display):
        text = self.font.render(str(self.count), True, (0, 0, 0))
        display.blit(self.image, self.rect)  # display the image (may be empty)
        # display.blit(text, self.rect.midright)  # display the count
