import imp
import time
import pygame

import player
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from particles import ParticleEffect
from magic import MagicPlayer
from upgrade import Upgrade
import intro_screen
# import globals


class Level:

    def __init__(self,data):

        self.player_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()


        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False


        image = pygame.image.load('graphics/player/down_idle/idle_down.png')
        pygame.display.update()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map(data)

        self.weapon_rect = pygame.rect.Rect((0,0),(0,0))
        self.last_item_time = 0
        # user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        # game over screen image
        self.gameover = pygame.image.load('graphics/test/gameover.png').convert_alpha()

        # inventory image
        self.inventory = pygame.image.load('graphics/test/inventory.png').convert_alpha()
  
    def return_player(self):
        return self.player

    def create_map(self,data):

        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'object': import_csv_layout('map/map_Objects.csv'),
            # 'entities': import_csv_layout('map/map_Entities.csv')
        }
        graphics = {
            'grass': import_folder('graphics/grass'),
            'objects': import_folder('graphics/objects')
        }

        self.player = Player(
                (int(data[3]),int(data[4])),
                [self.visible_sprites],
                self.obstacle_sprites,
                self.create_attack,
                self.destroy_attack,
                self.create_magic,data)


        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')

                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)

                        if style == 'entities':
                            if col == '394':

                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic,data)
                                pass

                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'

                                # Enemy(
                                #     monster_name,
                                #     (x, y),
                                #     [self.visible_sprites, self.attackable_sprites],
                                #     self.obstacle_sprites,
                                #     self.damage_player,
                                #     self.trigger_death_particles,
                                #     self.add_exp)


    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])
        self.weapon_rect = self.current_attack.rect

    def return_current_attack(self):
        return self.weapon_rect

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

        if style == 'crossbow':
            self.magic_player.arrow(self.player, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    # def player_attack_logic(self):
    #     if self.attack_sprites:
    #         for attack_sprite in self.attack_sprites:
    #             collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
    #             if collision_sprites:
    #                 for target_sprite in collision_sprites:
    #                     if target_sprite.sprite_type == 'grass':
    #                         pos = target_sprite.rect.center
    #                         offset = pygame.math.Vector2(0, 75)
    #                         for leaf in range(randint(3, 6)):
    #                             self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
    #                         target_sprite.kill()
    #                     else:
    #                         target_sprite.get_damage(self.player, attack_sprite.sprite_type)


    def damage_player(self, amount):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            # self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])


    def trigger_death_particles(self, pos, particle_type):

        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def add_exp(self, amount):

        self.player.exp += amount

    def toggle_menu(self):

        self.game_paused = not self.game_paused

    # item drops
    def add_water_potion_drop(self, inventory_rect):
        font = pygame.font.SysFont(WATER_COLOR, UI_FONT_SIZE)
        counter = font.render(str(self.player.num_water_potion), 1, TEXT_COLOR)
        self.display_surface.blit(counter, (inventory_rect.x+9, inventory_rect.y+8))


    def add_blood_potion_drop(self, inventory_rect):
        font = pygame.font.SysFont(WATER_COLOR, UI_FONT_SIZE)
        counter = font.render(str(self.player.num_blood_potion), 1, TEXT_COLOR)
        self.display_surface.blit(counter, (inventory_rect.x+73, inventory_rect.y+8))


    def add_coin_drop(self, inventory_rect):
        font = pygame.font.SysFont(WATER_COLOR, UI_FONT_SIZE)
        counter = font.render(str(self.player.num_coin), 1, TEXT_COLOR)
        self.display_surface.blit(counter, (inventory_rect.x+137, inventory_rect.y+8))


    def add_bamboo_drop(self, inventory_rect):
        font = pygame.font.SysFont(WATER_COLOR, UI_FONT_SIZE)
        counter = font.render(str(self.player.num_bamboo), 1, TEXT_COLOR)
        self.display_surface.blit(counter, (inventory_rect.x+201, inventory_rect.y+8))


    def use_water_potion(self):
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            if current_time - self.last_item_time > 3000:
                if self.player.num_water_potion > 0:
                    self.player.num_water_potion -= 1
                    self.player.energy += 10
                    self.last_item_time = current_time

    def use_blood_potion(self):
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_2]:
            if current_time - self.last_item_time > 3000:
                if self.player.num_blood_potion > 0:
                    self.player.num_blood_potion -= 1
                    self.player.health += 10
                    self.last_item_time = current_time

    def use_coin(self):
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_3]:
            if current_time - self.last_item_time > 3000:
                if self.player.num_coin > 0:
                    self.player.num_coin -= 1
                    self.player.exp += 1
                    self.last_item_time = current_time


    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        # draw inventory
        inventory_rect = pygame.Rect(0, 0, 1280, 1350)
        inventory_surf = self.inventory
        inventory_rect = inventory_surf.get_rect(center=inventory_rect.center)
        self.display_surface.blit(inventory_surf, inventory_rect)

        self.add_bamboo_drop(inventory_rect)
        self.add_coin_drop(inventory_rect)
        self.add_water_potion_drop(inventory_rect)
        self.add_blood_potion_drop(inventory_rect)

        self.use_coin()
        self.use_blood_potion()
        self.use_water_potion()
        
        if self.player.health <= 0:
            self.player.game_over = True

        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)

        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()

            # self.player_attack_logic()
  


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

        # if player enters area for first time
        # if it's the first time = 0, else = 1
        self.au = 0
        self.am = 0
        self.al = 0
        self.bu = 0
        self.bm = 0
        self.bl = 0
        self.cu = 0
        self.cm = 0
        self.cl = 0
        self.du = 0
        self.dm = 0
        self.dl = 0

    # def custom_draw(self, player):
    #
    #     # getting the offset
    #     self.offset.x = player.rect.centerx - self.half_width
    #     self.offset.y = player.rect.centery - self.half_height
    #
    #     # drawing the floor
    #     floor_offset_pos = self.floor_rect.topleft - self.offset
    #     self.display_surface.blit(self.floor_surf, floor_offset_pos)
    #
    #     # for sprite in self.sprites():
    #     for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
    #         offset_pos = sprite.rect.topleft - self.offset
    #         self.display_surface.blit(sprite.image, offset_pos)

        # loading the floor images commands

    def loadAu(self):
        self.floor_surf_Au = pygame.image.load('graphics/tilemap/Au.jpeg')
        self.floor_rect_Au = self.floor_surf_Au.get_rect(topleft=(0, 0))

    def loadAm(self):
        self.floor_surf_Am = pygame.image.load('graphics/tilemap/Am.jpeg')
        self.floor_rect_Am = self.floor_surf_Am.get_rect(topleft=(0, 7776))

    def loadAl(self):
        self.floor_surf_Al = pygame.image.load('graphics/tilemap/Al.jpeg')
        self.floor_rect_Al = self.floor_surf_Al.get_rect(topleft=(0, 16272))

    def loadBu(self):
        self.floor_surf_Bu = pygame.image.load('graphics/tilemap/Bu.jpeg')
        self.floor_rect_Bu = self.floor_surf_Bu.get_rect(topleft=(7040, 0))

    def loadBm(self):
        self.floor_surf_Bm = pygame.image.load('graphics/tilemap/Bm.jpeg')
        self.floor_rect_Bm = self.floor_surf_Bm.get_rect(topleft=(7040, 7776))

    def loadBl(self):
        self.floor_surf_Bl = pygame.image.load('graphics/tilemap/Bl.jpeg')
        self.floor_rect_Bl = self.floor_surf_Bl.get_rect(topleft=(7040, 16272))

    def loadCu(self):
        self.floor_surf_Cu = pygame.image.load('graphics/tilemap/Cu.jpeg')
        self.floor_rect_Cu = self.floor_surf_Cu.get_rect(topleft=(15360, 0))

    def loadCm(self):
        self.floor_surf_Cm = pygame.image.load('graphics/tilemap/Cm.jpeg')
        self.floor_rect_Cm = self.floor_surf_Cm.get_rect(topleft=(15360, 7776))

    def loadCl(self):
        self.floor_surf_Cl = pygame.image.load('graphics/tilemap/Cl.jpeg')
        self.floor_rect_Cl = self.floor_surf_Cl.get_rect(topleft=(15360, 16272))

    def loadDu(self):
        self.floor_surf_Du = pygame.image.load('graphics/tilemap/Du.jpeg')
        self.floor_rect_Du = self.floor_surf_Du.get_rect(topleft=(23680, 0))

    def loadDm(self):
        self.floor_surf_Dm = pygame.image.load('graphics/tilemap/Dm.jpeg')
        self.floor_rect_Dm = self.floor_surf_Dm.get_rect(topleft=(23680, 7776))

    def loadDl(self):
        self.floor_surf_Dl = pygame.image.load('graphics/tilemap/Dl.jpeg')
        self.floor_rect_Dl = self.floor_surf_Dl.get_rect(topleft=(23680, 16272))

    # drawing the floor
    def custom_draw(self, player):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # area A
        if 0 < player.rect.centerx < 7680:
            # upper
            if 0 < player.rect.centery < 8136:
                if self.au == 0:
                    self.loadAu()
                    self.au = 1
                floor_offset_pos_Au = self.floor_rect_Au.topleft - self.offset
                self.display_surface.blit(self.floor_surf_Au, floor_offset_pos_Au)
            # middle
            elif 8136 <= player.rect.centery < 16632:
                if self.am == 0:
                    self.loadAm()
                    self.am = 1
                floor_offset_pos_Am = self.floor_rect_Am.topleft - self.offset
                self.display_surface.blit(self.floor_surf_Am, floor_offset_pos_Am)
            # lower
            elif 16632 <= player.rect.centery < 24768:
                if self.al == 0:
                    self.loadAl()
                    self.al = 1
                floor_offset_pos_Al = self.floor_rect_Al.topleft - self.offset
                self.display_surface.blit(self.floor_surf_Al, floor_offset_pos_Al)

        # area B
        elif 7680 <= player.rect.centerx < 16000:
            # upper
            if 0 < player.rect.centery < 8136:
                if self.bu == 0:
                    self.loadBu()
                    self.bu = 1
                floor_offset_pos_Bu = self.floor_rect_Bu.topleft - self.offset
                self.display_surface.blit(self.floor_surf_Bu, floor_offset_pos_Bu)
            # middle
            elif 8136 <= player.rect.centery < 16632:
                if self.bm == 0:
                    self.loadBm()
                    self.bm = 1
                floor_offset_pos_Bm = self.floor_rect_Bm.topleft - self.offset
                self.display_surface.blit(self.floor_surf_Bm, floor_offset_pos_Bm)
            # lower
            elif 16632 <= player.rect.centery < 24768:
                if self.bl == 0:
                    self.loadBl()
                    self.bl = 1
                floor_offset_pos_Bl = self.floor_rect_Bl.topleft - self.offset
                self.display_surface.blit(self.floor_surf_Bl, floor_offset_pos_Bl)

        # area c
        elif 16000 <= player.rect.centerx < 24320:
            # upper
            if 0 < player.rect.centery < 8136:
                if self.cu == 0:
                    self.loadCu()
                    self.cu = 1
                floor_offset_pos_Cu = self.floor_rect_Cu.topleft - self.offset
                self.display_surface.blit(self.floor_surf_Cu, floor_offset_pos_Cu)
            # middle
            elif 8136 <= player.rect.centery < 16632:
                if self.cm == 0:
                    self.loadCm()
                    self.cm = 1
                floor_offset_pos_Cm = self.floor_rect_Cm.topleft - self.offset
                self.display_surface.blit(self.floor_surf_Cm, floor_offset_pos_Cm)
            # lower
            elif 16632 <= player.rect.centery < 24768:
                if self.cl == 0:
                    self.loadCl()
                    self.cl = 1
                floor_offset_pos_Cl = self.floor_rect_Cl.topleft - self.offset
                self.display_surface.blit(self.floor_surf_Cl, floor_offset_pos_Cl)

        # area d
        elif 24320 <= player.rect.centerx < 32000:
            # upper
            if 0 < player.rect.centery < 8136:
                if self.du == 0:
                    self.loadDu()
                    self.du = 1
                floor_offset_pos_Du = self.floor_rect_Du.topleft - self.offset
                self.display_surface.blit(self.floor_surf_Du, floor_offset_pos_Du)
            # middle
            elif 8136 <= player.rect.centery < 16632:
                if self.dm == 0:
                    self.loadDm()
                    self.dm = 1
                floor_offset_pos_Dm = self.floor_rect_Dm.topleft - self.offset
                self.display_surface.blit(self.floor_surf_Dm, floor_offset_pos_Dm)
            # lower
            elif 16632 <= player.rect.centery < 24768:
                if self.dl == 0:
                    self.loadDl()
                    self.dl = 1
                floor_offset_pos_Dl = self.floor_rect_Dl.topleft - self.offset
                self.display_surface.blit(self.floor_surf_Dl, floor_offset_pos_Dl)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
