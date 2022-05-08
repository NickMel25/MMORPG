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
from magic import MagicPlayer
from upgrade import Upgrade
import intro_screen

# import globals
from player import num_water_potion, num_blood_potion, num_coin, num_bamboo


class Level:
    def __init__(self):

        self.player_sprites = pygame.sprite.Group()

        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
        self.game_over = False

        image = pygame.image.load('graphics/player/down_idle/idle_down.png')
        pygame.display.update()
        self.path = []
        matrix = import_csv_layout('map/map_FloorBlocks.csv')
        self.matrix = matrix
        self.player = 0
        self.pathfind = 0

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

                        # if style == 'boundary':
                        # Tile((x, y), [self.obstacle_sprites], 'invisible')

                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)

                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    (x, y), self.path,
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
                                Enemy(
                                    monster_name,
                                    (x, y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    self.add_exp)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

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

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):

        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def add_exp(self, amount):

        self.player.exp += amount

    def toggle_menu(self):

        self.game_paused = not self.game_paused

    # item drops
    def add_water_potion_drop(self, inventory_rect):
        font = pygame.font.SysFont(WATER_COLOR, UI_FONT_SIZE)
        counter = font.render(str(player.num_water_potion), 1, TEXT_COLOR)
        self.display_surface.blit(counter, (inventory_rect.x + 9, inventory_rect.y + 8))

    def add_blood_potion_drop(self, inventory_rect):
        font = pygame.font.SysFont(WATER_COLOR, UI_FONT_SIZE)
        counter = font.render(str(player.num_blood_potion), 1, TEXT_COLOR)
        self.display_surface.blit(counter, (inventory_rect.x + 73, inventory_rect.y + 8))

    def add_coin_drop(self, inventory_rect):
        font = pygame.font.SysFont(WATER_COLOR, UI_FONT_SIZE)
        counter = font.render(str(player.num_coin), 1, TEXT_COLOR)
        self.display_surface.blit(counter, (inventory_rect.x + 137, inventory_rect.y + 8))

    def add_bamboo_drop(self, inventory_rect):
        font = pygame.font.SysFont(WATER_COLOR, UI_FONT_SIZE)
        counter = font.render(str(player.num_bamboo), 1, TEXT_COLOR)
        self.display_surface.blit(counter, (inventory_rect.x + 201, inventory_rect.y + 8))

    def use_water_potion(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            if player.num_water_potion > 0:
                player.num_water_potion -= 1
                self.player.energy += 10

    def use_blood_potion(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_2]:
            if player.num_blood_potion > 0:
                player.num_blood_potion -= 1
                self.player.health += 10

    def use_coin(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_3]:
            if player.num_coin > 0:
                player.num_coin -= 1
                self.player.exp += 1

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
        self.use_water_potion()
        self.use_blood_potion()
        self.use_coin()

        if self.player.health <= 0:
            self.game_over = True
            self.game_over_screen()

        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()

    def restart(self):
        self.player.pos = (2112, 1344)
        self.player.status = 'down'

        self.player.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5}
        self.player.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic': 10, 'speed': 10}
        self.player.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic': 100, 'speed': 100}
        self.player.health = self.player.stats['health'] * 0.5
        self.player.energy = self.player.stats['energy'] * 0.8
        self.player.exp = 0
        self.player.speed = self.player.stats['speed']
        self.path = []
        player.num_water_potion = 0
        player.num_blood_potion = 0
        player.num_coin = 0
        player.num_bamboo = 0

    def game_over_screen(self):

        if self.game_over:
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

            # stop the player
            self.player.pressed_mouse_pos = -1

    def path_found(self, mouse):
        self.player.pressed_mouse_pos = mouse
        self.player.in_time_location_x = self.player.rect.centerx
        self.player.in_time_location_y = self.player.rect.centery


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf_Au = pygame.image.load('graphics/tilemap/groundAu.png').convert()
        self.floor_surf_Al = pygame.image.load('graphics/tilemap/groundAl.png').convert()
        self.floor_surf_Bu = pygame.image.load('graphics/tilemap/groundBu.png').convert()
        self.floor_surf_Bl = pygame.image.load('graphics/tilemap/groundBl.png').convert()
        self.floor_surf_Cu = pygame.image.load('graphics/tilemap/groundCu.png').convert()
        self.floor_surf_Cl = pygame.image.load('graphics/tilemap/groundCl.png').convert()
        self.floor_rect_Au = self.floor_surf_Au.get_rect(topleft=(0, 0))
        self.floor_rect_Al = self.floor_surf_Al.get_rect(topleft=(0, 12024))
        self.floor_rect_Bu = self.floor_surf_Bu.get_rect(topleft=(10240, 0))
        self.floor_rect_Bl = self.floor_surf_Bl.get_rect(topleft=(10240, 12024))
        self.floor_rect_Cu = self.floor_surf_Cu.get_rect(topleft=(20480, 0))
        self.floor_rect_Cl = self.floor_surf_Cl.get_rect(topleft=(20480, 12024))

    def custom_draw(self, player):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        # drawing the floor
        # area A
        if 0 < player.rect.centerx < 10880:
            # upper
            if 0 < player.rect.centery < 12384:
                floor_offset_pos_Au = self.floor_rect_Au.topleft - self.offset
                self.display_surface.blit(self.floor_surf_Au, floor_offset_pos_Au)
            # lower
            elif 12384 <= player.rect.centery < 24768:
                floor_offset_pos_Al = self.floor_rect_Al.topleft - self.offset
                self.display_surface.blit(self.floor_surf_Al, floor_offset_pos_Al)
        # area B
        elif 10880 <= player.rect.centerx < 21120:
            # upper
            if 0 < player.rect.centery < 12384:
                floor_offset_pos_Bu = self.floor_rect_Bu.topleft - self.offset
                self.display_surface.blit(self.floor_surf_Bu, floor_offset_pos_Bu)
            # lower
            elif 12384 <= player.rect.centery < 24768:
                floor_offset_pos_Bl = self.floor_rect_Bl.topleft - self.offset
                self.display_surface.blit(self.floor_surf_Bl, floor_offset_pos_Bl)

        # area C upper
        elif 0 < player.rect.centery < 12384:
            floor_offset_pos_Cu = self.floor_rect_Cu.topleft - self.offset
            self.display_surface.blit(self.floor_surf_Cu, floor_offset_pos_Cu)
        # area C lower
        else:
            floor_offset_pos_Cl = self.floor_rect_Cl.topleft - self.offset
            self.display_surface.blit(self.floor_surf_Cl, floor_offset_pos_Cl)

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
