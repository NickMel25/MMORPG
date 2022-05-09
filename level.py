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

    def __init__(self):

        self.player_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
        self.game_over = False

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
        self.create_map()

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

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'object': import_csv_layout('map/map_Objects.csv'),
            'entities': import_csv_layout('map/map_Entities.csv')
        }
        graphics = {
            'grass': import_folder('graphics/grass'),
            'objects': import_folder('graphics/objects')
        }
        username = intro_screen.main()

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
                                    self.create_magic, username)
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

    def return_current_attack(self):
        return self.current_attack.rect

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

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

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
        self.display_surface.blit(counter, (inventory_rect.x + 9, inventory_rect.y + 8))

    def add_blood_potion_drop(self, inventory_rect):
        font = pygame.font.SysFont(WATER_COLOR, UI_FONT_SIZE)
        counter = font.render(str(self.player.num_blood_potion), 1, TEXT_COLOR)
        self.display_surface.blit(counter, (inventory_rect.x + 73, inventory_rect.y + 8))

    def add_coin_drop(self, inventory_rect):
        font = pygame.font.SysFont(WATER_COLOR, UI_FONT_SIZE)
        counter = font.render(str(self.player.num_coin), 1, TEXT_COLOR)
        self.display_surface.blit(counter, (inventory_rect.x + 137, inventory_rect.y + 8))

    def add_bamboo_drop(self, inventory_rect):
        font = pygame.font.SysFont(WATER_COLOR, UI_FONT_SIZE)
        counter = font.render(str(self.player.num_bamboo), 1, TEXT_COLOR)
        self.display_surface.blit(counter, (inventory_rect.x + 201, inventory_rect.y + 8))

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

        if self.player.health <= 0:
            self.game_over = True

            # show image "game over"
            bg_rect = pygame.Rect(0, 0, 1280, 720)
            gameover_surf = self.gameover
            gameover_rect = gameover_surf.get_rect(center=bg_rect.center)
            self.display_surface.blit(gameover_surf, gameover_rect)

            # draw button to restart game
            pygame.draw.rect(self.display_surface, UI_BG_COLOR, [540, 385, 80, 30])
            smallfont = pygame.font.SysFont(UI_FONT, 16)
            text = smallfont.render('RESTART', True, TEXT_COLOR)
            self.display_surface.blit(text, (552.5, 395))

            # draw quit button
            pygame.draw.rect(self.display_surface, UI_BG_COLOR, [660, 385, 80, 30])
            smallfont = pygame.font.SysFont(UI_FONT, 16)
            text = smallfont.render('QUIT', True, TEXT_COLOR)
            self.display_surface.blit(text, (685, 395))

        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.player_attack_logic()

    def restart_location(self):
        self.player = ''


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

    def custom_draw(self, player):

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def players_draw(self, players):
        pass

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
