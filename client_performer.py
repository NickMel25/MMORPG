import pygame
from fake_entities import *
import main

players = {}
rect = ''
player_stats = ''

enemy_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

temp_group = pygame.sprite.Group()
temp_enemy_group = pygame.sprite.Group()

offset = pygame.math.Vector2()


def append(data):
    print(data)
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
    time_to_move = data[6]
    the_player_it_goes_to = data[7][1:-1]

    players_name = the_player_it_goes_to.split(',')[0]
    players_name = players_name[1:-1]

    players_location = str(the_player_it_goes_to.split(',')[1] + the_player_it_goes_to.split(',')[2])
    players_location = players_location.replace(' ', ',')
    players_location = players_location[1:]

    if not (players_location == ''):
        players_location = players_location[1:-1]
        players_location = list(map(int, players_location.split(',')))

    display_surface = pygame.display.get_surface()
    half_width = display_surface.get_size()[0] // 2
    half_height = display_surface.get_size()[1] // 2

    current_enemy = enemy_exists(id)
    if current_enemy == '':
        current_enemy = fake_monster(type, health, location, id, is_moving, players_location)
        enemy_group.add(current_enemy)

    else:
        current_enemy.set_moving_and_location(location, is_moving)
        current_enemy.set_destination(players_location)

    temp_enemy_group.add(current_enemy)

    enemy_rect = current_enemy.rect

    offset.x = player.rect.centerx - half_width
    offset.y = player.rect.centery - half_height

    enemy_offset = enemy_rect.topleft

    current_enemy.location(enemy_offset)
    temp_enemy_group.update()

    level.enemy_sprites.add(current_enemy)
    level.visible_sprites.add(current_enemy)

    temp_enemy_group.remove(current_enemy)
    pass
