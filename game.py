# John 3:5

# Mitchell Martin
# 12/21/2022
# Pixel2PGame Project



import pygame
import random

from backdrop import BackDrop
from settings import Settings
from player import Player
from player2 import SecondPlayer
from open_world import World
from enemy import Enemy
from pygame.locals import *

class FullGame:
    """This class contols the entire game."""
    def __init__(self):
        """This class controls the game."""
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_size))
        pygame.display.set_caption("1 Chronicles")
        self.display = pygame.Surface((390, 156))

        self.bg = BackDrop(self)
        self.world = World(self)

        self.particles = []

        self.fountains = pygame.sprite.Group()


        self.clock = pygame.time.Clock()

        self.players = pygame.sprite.Group()
        self.player = Player(self)
        self.player_2 = Player(self)
        self.player_2 = SecondPlayer(self)
        self.players.add(self.player_2)
        self.players.add(self.player)

        self.p1_points = 1
        self.p2_points = 0

        self.enemies = pygame.sprite.Group()

    def event_handling(self):
        """This method handles the events."""
        for event in pygame.event.get():
            if event.type == pygame.K_q:
                exit()
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.K_DOWN:
                self.keydown_events(event)

    def check_scroll(self):
        if self.p1_points > self.p2_points:
            self.scroll(self.player)
        else:
            self.scroll(self.player_2)

    def enemy_generation(self):
        """This method creates enemies."""
        while len(self.enemies) < 40:
            self.enemies.add(Enemy(self, random.randint(400, 4000), random.randint(300, 4000)))

    def enemy_collision(self):
        """This method handles enemy collisions."""
        collide = pygame.sprite.spritecollideany(self.player, self.enemies)
        if collide:
            self.p1_points -= 1
            if self.player.vel.x > 0:
                self.player.vel.x -= 2
                self.player.vel.y -= 1
            else:
                self.player.vel.x += 2
                self.player.vel.y -= 1

        collide_2 = pygame.sprite.spritecollideany(self.player_2, self.enemies)
        if collide_2:
            self.p2_points -= 1
            if self.player_2.vel.x > 0:
                self.player_2.vel.x -= 2
                self.player_2.vel.y -= 1
            else:
                self.player_2.vel.x += 2   
                self.player_2.vel.y -= 1      

    def collide_test(self, tiles):
        for player in self.players:
            for tile in tiles:

                if tile.colliderect(player.rect.x, player.rect.y + player.vel.y, player.image.get_width(), player.image.get_height()):
                    if player.vel.y < 0:
                        player.acc.y = tile.bottom - player.rect.top
                        player.vel.y = 1

                    elif player.vel.y >= 0:
                        player.acc.y = tile.top - player.rect.bottom
                        player.pos.y = tile.top + 1
                        player.vel.y = 0
                    
                    # if player.vel.x < 0:
                    #     player.rect.left = tile.right
                    # elif player.vel.x > 0:
                    #     player.rect.right = tile.left


    def jump(self):
        """This method control's the player's jump."""
        moving = pygame.key.get_pressed()
        for tile in self.world.blocks:
            col1 = tile.colliderect(self.player.rect.x, self.player.rect.y + self.player.vel.y, self.player.image.get_width(), self.player.image.get_height())
            col2 = tile.colliderect(self.player_2.rect.x, self.player_2.rect.y + self.player_2.vel.y, self.player_2.image.get_width(), self.player_2.image.get_height())
            if col1:
                if moving[pygame.K_UP]:
                    self.player.pos.y -= 1
                    self.player.vel.y = -self.settings.jump_height
            if col2:
                if moving[pygame.K_w]:
                    self.player_2.pos.y -= 1
                    self.player_2.vel.y = -(self.settings.jump_height + 0.5)
            

    def keydown_events(self, event):
        """This method handles key events."""
        if event.key == pygame.K_ESCAPE:
            exit()


    def run_game(self):
        """This method runs the game."""
        while True:

            self.clock.tick(60)
            self.update_game()
            for player in self.players:
                player.update()
            self.jump()
            self.enemy_generation()
            for enem in self.enemies:
                enem.update()
                enem.block_collision(self.world.blocks, self.enemies)
            self.enemy_collision()
            self.collide_test(self.world.blocks)
            self.players_collision()
            self.event_handling()
            self.check_scroll()



    def players_collision(self):
        """This method handles player collisions"""
        if self.player.rect.colliderect(self.player_2.rect):
            if self.player.vel.x < 0:
                self.player.vel.x += 2
                self.player.vel.y -= 1

                self.player_2.vel.x -= 2
                self.player_2.vel.y -= 1
            elif self.player.vel.x > 0:
                self.player.vel.x -= 2
                self.player.vel.y -= 1

                self.player_2.vel.x += 2
                self.player_2.vel.y -= 1            

    def scroll(self, player):
        """This method controls the scroll settings"""
        self.settings.scr[0] += (player.rect.x-self.settings.scr[0]-(390 / 2))/20
        self.settings.scr[1] += (player.rect.y-self.settings.scr[1]-(156 / 1.95))//20

    def create_fountain(self, xx, yy, color):
        """This method creates a fountain."""
        x = (xx - self.settings.scr[0])
        y = (yy - self.settings.scr[1])
        
        self.particles.append([[x,y], [random.randint(0,10)/ 10 -1, -3], random.randint(3,6)])

        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1
            pygame.draw.circle(self.display, color, [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                self.particles.remove(particle)

    
    def create_fountains(self):
        self.color = (0, 50, 190)

        self.create_fountain(self.player.pos.x,self.player.pos.y, self.color)
        self.create_fountain(self.player_2.pos.x,self.player_2.pos.y, self.color)
    


    def update_game(self):
        """This method updates the game"""
        self.screen.fill(self.settings.bg_color)
        self.display.fill(self.settings.bg_color)
        self.bg.blitme()
        self.create_fountains()



        self.world.draw()
        for player in self.players:
            player.blitme()
        for enem in self.enemies:
            enem.blitme()

        surf = pygame.transform.scale(self.display, self.settings.screen_size)

        self.screen.blit(surf, (0, 0))
        pygame.display.update()

if __name__ == '__main__':
    fg = FullGame()
    fg.run_game()