import pygame
from pygame.sprite import Sprite

vec = pygame.math.Vector2

class SecondPlayer(Sprite):
    
    def __init__(self, game):
        """This class handles the player."""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.display = game.display
        
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.Surface((5, 10)).convert()
        self.image.fill((200, 120, 150))
        self.rect = self.image.get_rect(midbottom=(5,3))

        self.pos = vec((340, 300))

        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def update(self):
        """This method controls the player's position."""
        self.acc = vec(0, 0.3)
        
        moving = pygame.key.get_pressed()
        if moving[pygame.K_a]:
            self.acc.x = -(self.settings.acceleration - 0.1)
        if moving[pygame.K_d]:
            self.acc.x = (self.settings.acceleration - 0.1)
        if moving[pygame.K_s]:
            self.acc.y = self.settings.acceleration

        self.acc.x += self.vel.x * self.settings.friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > (self.settings.screen_width * 2):
            self.pos.x = 0

        if self.pos.x < 0:
            self.pos.x = (self.settings.screen_width * 2)

        if self.pos.y > (self.settings.screen_height + 3000):
            self.pos.y = 0

        self.rect.midbottom = self.pos

    def blitme(self):
        """This method displays the player upon the screen."""
        self.display.blit(self.image, (self.rect.x-self.settings.scr[0], self.rect.y-self.settings.scr[1]))