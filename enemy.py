import pygame
from pygame.sprite import Sprite

vec = pygame.math.Vector2

class Enemy(Sprite):

    def __init__(self, game, x, y):
        """This class controls the enemy."""
        super().__init__()
        self.display = game.display
        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = self.screen.get_rect()

        self.image = pygame.Surface((10, 20)).convert_alpha()
        self.image.fill((200, 0, 100))
        self.rect = self.image.get_rect(midbottom=(10, 20))

        self.pos = ((x,y))
        self.acc = vec(0,0)
        self.vel = vec(0,0)

    def update(self):
        self.acc.x = (-self.settings.acceleration) - 0.1

        self.acc.x += self.vel.x * self.settings.friction
        self.vel += (0, 0.4)
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.y > (self.settings.screen_height + 2500):
            self.pos.y = -10
        
        self.rect.midbottom = self.pos
    
    def block_collision(self, blocks, grp):
        for block in blocks:
            if self.rect.colliderect(block):
                if self.vel.y > 0:
                    if self.pos.y < block.bottom:
                        self.pos.y = block.top + 1
                        self.vel.y = 0
            
        if self.pos.y > (self.settings.screen_height + 2500):
            grp.kill()
    
    def blitme(self):
        """This method displays the enemy on the screen."""
        self.display.blit(self.image, (self.rect.x-self.settings.scr[0], self.rect.y-self.settings.scr[1]))
