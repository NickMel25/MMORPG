import pygame
from config import *


class SpriteSheet:
    def __init__(self, file):
        super().__init__()
        self.sheet = pygame.image.load(file)
        self.sheet.set_colorkey((255, 255, 255))
        self.sheet = self.sheet.convert_alpha()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites)
        self.game = game
        self._layer = PLAYER_LAYER  # tells pygame which layer the player will be in
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.sheet_coords = (3, 2)
        self.moving = False
        self.frame = 0

        self.width = TILESIZE
        self.height = TILESIZE
        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        if self.moving:
            self.frame = (self.frame + 0.1) % 3
            sheet_x, sheet_y = self.sheet_coords
            self.image = self.game.character_spritesheet.get_sprite(sheet_x + int(self.frame) * self.width, sheet_y,
                                                                    self.width, self.height)

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        self.moving = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
            self.sheet_coords = (3, 3 * self.height+2.5)
        elif keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
            self.sheet_coords = (3, 2 * self.height+2.5)
        elif keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
            self.sheet_coords = (3, self.height+2.5)
        elif keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'
            self.sheet_coords = (3, 2)
        else:
            self.moving = False

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
        if self.rect.x < 0:
            self.rect.x = 0

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
        if self.rect.y < 0:
            self.rect.y = 0


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites)
        self.game = game
        self._layer = GROUND_LAYER

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64, 352, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites, game.blocks)
        self.game = game
        self._layer = BLOCK_LAYER
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(960, 440, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Water(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites, game.blocks)
        self.game = game
        self._layer = BLOCK_LAYER

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(865, 159, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y













