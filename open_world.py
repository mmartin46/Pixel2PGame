import pygame
import csv
from pygame.sprite import Sprite

class World(Sprite):
    """This class handles the game world."""
    
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.display = game.display

        self.block_size = 10

        map_0 = 'maps/completemap.csv'
        map_1 = 'maps\\big_map.csv'
        self.full_map = []

        with open(map_1) as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                self.full_map.append(list(row))

        self.grass_block = pygame.image.load('sprites\grass_tile.png').convert_alpha()
        self.block = pygame.image.load('sprites\\block_tile.png').convert_alpha()

    def draw(self):
        """This method creates the world."""
        self.blocks = []
        for y, line in enumerate(self.full_map):
            for x, c in enumerate(line):
                if c == "0":
                    center = ((x*self.block_size)+4, (y*self.block_size)+4)
                    self.display.blit(self.grass_block, (x * self.block_size-self.settings.scr[0], y * self.block_size-self.settings.scr[1]))
                    self.blocks.append(self.grass_block.get_rect(center=center))
