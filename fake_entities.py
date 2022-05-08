import math

import pygame
from settings import monster_data

class fake_player(pygame.sprite.Sprite):
    def __init__(self, name) -> None:
        super().__init__()
        self.image = pygame.image.load('graphics/player/down_idle/idle_down.png')
        self.rect = self.image.get_rect()
        self.name = name
        self.next_location = (0,0)
        self.image_path = ''
    
    def change_image(self,animation,frame):
        self.image_path = animation[int(frame)]

    def location(self,location):
        self.next_location = location

    def update(self):
        self.rect.topleft = self.next_location
        # self.image = pygame.image.load(self.image_path)
        self.image = self.image_path


class fake_monster(pygame.sprite.Sprite):
    def __init__(self, name, hp, location, id, moving, the_player_it_goes_to) -> None:
        super().__init__()
        if name == "bamboo":
            self.image = pygame.image.load('graphics/monsters/bamboo/idle/0.png')
        if name == "squid":
            self.image = pygame.image.load('graphics/monsters/squid/idle/0.png')
        if name == "raccoon":
            self.image = pygame.image.load('graphics/monsters/raccoon/idle/0.png')
        if name == "spirit":
            self.image = pygame.image.load('graphics/monsters/spirit/idle/0.png')

        self.isdead = False
        self.hp = hp
        self.rect = self.image.get_rect()
        self.rect.topleft = location
        self.name = name
        self.next_location = location
        self.image_path = ''
        self.id = id
        self.is_moving = moving
        self.the_player_it_goes_to = the_player_it_goes_to
        self.speed = monster_data[name]['speed']

    def is_dead(self):
        if self.hp <= 0:
            self.isdead = True

    def location(self, location):
        self.next_location = location

    def update(self):
         self.rect.topleft = self.next_location

    def enemy_update(self):
        pass

    def set_moving_and_location(self, location, moving):
        self.next_location = location
        self.is_moving = moving

    def set_destination(self, the_player_it_goes_to):
        self.the_player_it_goes_to = the_player_it_goes_to
