import pygame
from settings import *
from random import randint


class MagicPlayer:

    def __init__(self, animation_player):
        self.animation_player = animation_player

    def heal(self, player, strength, cost, groups):

        self.magic_type = 'heal'

        if player.energy >= cost:
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles('aura', player.rect.center, groups)
            self.animation_player.create_particles('heal', player.rect.center, groups)

    def flame(self, player, cost, groups):
        self.magic_type = 'flame'

        if player.energy >= cost:
            player.energy -= cost

            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1, 0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1, 0)
            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0, -1)
            else:
                direction = pygame.math.Vector2(0, 1)

            width = 0
            height = 0
            for i in range(1, 6):
                if direction.x:  # horizontal
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x, y), groups)
                else:  # vertical
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x, y), groups)

                if i == 1:
                    if player.status.split('_')[0] == 'right':
                        width = 30 * 9
                        height = 48
                    elif player.status.split('_')[0] == 'left':
                        width = 30 * 9
                        height = 48
                    elif player.status.split('_')[0] == 'up':
                        width = 48
                        height = 30 * 9
                    else:
                        width = 48
                        height = 30 * 9
                elif i == 5:
                    if player.status.split('_')[0] == 'right':
                        width = 30 * 9
                        height = 48
                    elif player.status.split('_')[0] == 'left':
                        width = 30 * 9
                        height = 48
                    elif player.status.split('_')[0] == 'up':
                        width = 48
                        height = 30 * 9
                    else:
                        width = 48
                        height = 30 * 9

            player.magic_rect = pygame.rect.Rect(player.rect.topleft, (width, height))
        # player.is_magic = False


    def arrow(self, player, groups):
        if player.status.split('_')[0] == 'right':
            direction = pygame.math.Vector2(1, 0)
        elif player.status.split('_')[0] == 'left':
            direction = pygame.math.Vector2(-1, 0)
        elif player.status.split('_')[0] == 'up':
            direction = pygame.math.Vector2(0, -1)
        else:
            direction = pygame.math.Vector2(0, 1)

        width = 0
        height = 0
        for i in range(1, 6):

            if direction.x:  # horizontal
                offset_x = (direction.x * i) * TILESIZE
                x = player.rect.centerx + offset_x
                y = player.rect.centery
                if player.status.split('_')[0] == 'left':
                    self.animation_player.create_particles('arrow_left', (x, y), groups)
                else:
                    self.animation_player.create_particles('arrow_right', (x, y), groups)

            else:  # vertical
                offset_y = (direction.y * i) * TILESIZE
                x = player.rect.centerx
                y = player.rect.centery + offset_y
                if player.status.split('_')[0] == 'up':
                    self.animation_player.create_particles('arrow_up', (x, y), groups)
                else:
                    self.animation_player.create_particles('arrow_down', (x, y), groups)

            if i == 1:
                if player.status.split('_')[0] == 'right':
                    width = 32 * 9
                    height = 44
                elif player.status.split('_')[0] == 'left':
                    width = 32 * 9
                    height = 44
                elif player.status.split('_')[0] == 'up':
                    width = 44
                    height = 32 * 9
                else:
                    width = 44
                    height = 32 * 9
            if i == 5:
                if player.status.split('_')[0] == 'right':
                    width = 32 * 9
                    height = 44
                elif player.status.split('_')[0] == 'left':
                    width = 32 * 9
                    height = 44
                elif player.status.split('_')[0] == 'up':
                    width = 44
                    height = 32 * 9
                else:
                    width = 44
                    height = 32 * 9

        player.magic_rect = pygame.rect.Rect(player.rect.topleft, (width, height))
    