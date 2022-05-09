
import random

import pygame
from fake_entities import *
last_hurt = 0

players = {}
rect = ''
player_stats = ''

enemy_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

temp_group = pygame.sprite.Group()
temp_enemy_group = pygame.sprite.Group()

offset = pygame.math.Vector2()


def append(data):
    temp = ''
    answers = data.split(":")
    info_list = {}
    players[answers[0]] = info_list
    info_list["username"] = answers[0]
    info_list["status"] = answers[1]
    info_list["attacking"] = answers[2]
    temp = answers[3][1:-1]
    temp = tuple(map(int, temp.split(',')))
    info_list["location"] = temp
    info_list["hitbox"] = answers[4]
    info_list["frame"] = answers[5]
    info_list["connection"] = data[1]


def update(rect, location):
    rect.center = location


def user_exists(user):
    for sprite in player_group:
        if sprite.name == user:
            return sprite
    return ''


def return_user_offset(offset, user_location):
    return user_location - offset


def display_players(data, player, level):
    global rect

    append(data)
    username = data.split(':')[0]
    display_surface = pygame.display.get_surface()
    half_width = display_surface.get_size()[0] // 2
    half_height = display_surface.get_size()[1] // 2

    # prepares and adds the fake player to a group
    current_user = user_exists(username)
    if '' == current_user:
        current_user = fake_player(username)
        player_group.add(current_user)
    temp_group.add(current_user)

    user_rect = tuple(map(int, data.split(':')[4][6:-2].split(', ')))
    user_rect = pygame.Rect((user_rect[0], user_rect[1]), (user_rect[2], user_rect[3]))

    offset.x = player.rect.centerx - half_width
    offset.y = player.rect.centery - half_height

    user_offset = user_rect.topleft

    animation = player.animations[players[username]["status"]]

    # character_path = 'graphics/player/'
    current_user.change_image(animation, players[username]["frame"])
    current_user.location(user_offset)
    temp_group.update()

    level.player_sprites.add(current_user)
    level.visible_sprites.add(current_user)

    temp_group.remove(current_user)
    pass


# ======================================================================================================================
# ---------------------------------------------------------MONSTER PERFORMER--------------------------------------------
# ======================================================================================================================


def get_player(playe, leve):
    global player
    global level
    player = playe
    level = leve


def enemy_exists(id):
    for sprite in enemy_group:
        if sprite.id == id:
            return sprite
    return ''


def print_monsters_around_player(data):
    global last_hurt

    type = data[0]
    health = data[1]
    moving = data[2]

    is_moving = False
    if (moving == 'True'):
        is_moving = True

    location = data[3][1:-1]
    location = list(map(float, location.split(',')))

    id = data[4]
    is_attacking = data[5]
    should_player_get_damage = data[6]

    if should_player_get_damage == 'True':
        level.damage_player(10)

    the_player_it_goes_to = data[7][1:-1]

    display_surface = pygame.display.get_surface()
    half_width = display_surface.get_size()[0] // 2
    half_height = display_surface.get_size()[1] // 2

    current_enemy = enemy_exists(id)
    if current_enemy == '':
        current_enemy = fake_monster(type, health, location, id, is_moving, the_player_it_goes_to)
        enemy_group.add(current_enemy)

    else:
        current_enemy.set_moving_and_location(location, is_moving)

    temp_enemy_group.add(current_enemy)

    enemy_rect = current_enemy.rect

    offset.x = player.rect.centerx - half_width
    offset.y = player.rect.centery - half_height

    enemy_offset = enemy_rect.topleft

    temp_enemy_group.update()

    level.enemy_sprites.add(current_enemy)
    level.visible_sprites.add(current_enemy)

    if health == '0':
        level.visible_sprites.remove(current_enemy)

    temp_enemy_group.remove(current_enemy)

    pass


def get_the_stuff():
    random_number = random.randint(1, 4)
    if random_number == 1:
        player.num_coin += 1
    elif random_number == 2:
        player.num_water_potion += 1
    elif random_number == 3:
        player.num_blood_potion += 1
    else:
        player.num_bamboo += 1

    random_number = random.randint(1, 4)
    if random_number == 1:
        player.num_coin += 1
    elif random_number == 2:
        player.num_water_potion += 1
    elif random_number == 3:
        player.num_blood_potion += 1
    else:
        player.num_bamboo += 1
