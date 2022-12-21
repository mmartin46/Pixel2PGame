import pygame

class BackDrop:

    def __init__(self, game):
        """This class controls the background."""
        self.screen = game.screen
        self.display = game.display

        self.image = pygame.image.load('C:/Users/agini/Desktop/full_world_game/oh/Pixel2PGame/images/fullbg.png').convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.y = -100

    def blitme(self):
        """This method displays the background."""
        self.display.blit(self.image, self.rect)