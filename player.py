import pygame
from settings import *
from support import import_folder
from entity import Entity
from pathfinder import *

# items
num_water_potion = 0
num_blood_potion = 0
num_coin = 0
num_bamboo = 0


class Player(Entity):
    def __init__(self, pos, empty_path, groups, obstacle_sprites, create_attack, destroy_attack, create_magic, username):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['player'])

        self.chat_paused = False
        self.display_surface = pygame.display.get_surface()
        self.username = username

        # graphics setup
        self.import_player_assets()
        self.status = 'down'

        # movement
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        self.path = []
        self.collision_rects = []
        self.empty_path = empty_path
        self.pos = self.hitbox.center

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5}
        self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic': 10, 'speed': 10}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic': 100, 'speed': 100}
        self.health = self.stats['health'] * 0.5
        self.energy = self.stats['energy'] * 0.8
        self.exp = 0
        self.speed = self.stats['speed']

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def set_path(self, path):
        self.path = path
        self.create_collision_rects()
        self.get_direction()

    def create_collision_rects(self):
        if self.path:
            self.collision_rects = []
            for point in self.path:
                x = (point[0] * 64) + 32
                y = (point[1] * 64) + 32
                rect = pygame.Rect((x - 32, y - 32), (64, 64))
                self.collision_rects.append(rect)

    def get_direction(self):
        if self.collision_rects:
            start = pygame.math.Vector2(self.pos)
            end = pygame.math.Vector2(self.collision_rects[0].center)
            self.direction = (end - start).normalize()
            self.direction.y = round(self.direction.y)
            self.direction.x = round(self.direction.x)
            if self.direction.y == -1:
                self.status = 'up'
            elif self.direction.y == 1:
                self.status = 'down'
            else:
                self.direction.y = 0

            if self.direction.x == 1:
                self.status = 'right'
            elif self.direction.x == -1:
                self.status = 'left'
            else:
                self.direction.x = 0

        else:
            self.direction = pygame.math.Vector2(0, 0)
            self.path = []

    def check_collisions(self):
        if self.collision_rects:
            for rect in self.collision_rects:
                if rect.collidepoint(self.pos):
                    del self.collision_rects[0]
                    self.get_direction()
        else:
            self.path = []

    def empty_path(self):
        self.path = []

    def update_position(self):
        self.pos += self.direction * self.speed
        self.check_collisions()
        self.hitbox.center = self.pos

    def input(self):
        if not self.attacking:
            if not self.chat_paused:
                keys = pygame.key.get_pressed()

                # attack input
                if keys[pygame.K_SPACE] and self.health > 0:
                    self.attacking = True
                    self.attack_time = pygame.time.get_ticks()
                    self.create_attack()
                    if self.weapon_index == 5:
                        style = 'crossbow'
                        strength = 60
                        cost = 0
                        self.create_magic(style, strength, cost)

                # magic input
                if keys[pygame.K_LCTRL] and self.health > 0:
                    self.attacking = True
                    self.attack_time = pygame.time.get_ticks()
                    style = list(magic_data.keys())[self.magic_index]
                    strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                    cost = list(magic_data.values())[self.magic_index]['cost']
                    self.create_magic(style, strength, cost)

                if keys[pygame.K_q] and self.can_switch_weapon:
                    self.can_switch_weapon = False
                    self.weapon_switch_time = pygame.time.get_ticks()

                    if self.weapon_index < len(list(weapon_data.keys())) - 1:
                        self.weapon_index += 1
                    else:
                        self.weapon_index = 0

                    self.weapon = list(weapon_data.keys())[self.weapon_index]

                if keys[pygame.K_e] and self.can_switch_magic:
                    self.can_switch_magic = False
                    self.magic_switch_time = pygame.time.get_ticks()

                    if self.magic_index < len(list(magic_data.keys())) - 1:
                        self.magic_index += 1
                    else:
                        self.magic_index = 0

                    self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):

        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.003 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()

# <<<<<<< HEAD
#         self.animate()
#         self.move(self.stats['speed'])
# =======
        self.update_position()
        self.animate()

    #    self.move(self.stats['speed'])
        self.energy_recovery()

    def to_string(self):
        #              username :direction(string):is attacking: location (int)  : hitbox
        return f"{self.username}:{self.status}:{self.attacking}:{self.rect.topleft}:{self.hitbox}:{self.frame_index}"