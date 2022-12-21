import pygame

class Settings:
    def __init__(self):
        """This class controls the settings."""
        self.screen_height = 520
        self.screen_width = 1300
        self.screen_size = ((1300, 520))
        self.scr = [0,0]

        self.bg_color = (140, 190, 203)

        self.acceleration = 0.5
        self.friction = -0.12
        self.jump_height = 6