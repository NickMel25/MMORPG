import pygame
from fake_player import fake_player

players = {}
rect = ''
player_stats = ''

player_group = pygame.sprite.Group()
temp_group = pygame.sprite.Group()

offset = pygame.math.Vector2()

def append(data):
    print(data)
    temp = ''
    answers = data.split(":")
    info_list = {}
    players[answers[0]]= info_list
    info_list["username"] = answers[0]
    info_list["status"] = answers[1]
    info_list["attacking"] = answers[2]
    temp = answers[3][1:-1]
    temp =  tuple(map(int, temp.split(',')))
    info_list["location"] = temp
    info_list["hitbox"] = answers[4]
    info_list["frame"] = answers[5]
    info_list["connection"] = data[1]

def update(rect,location):
    rect.center = location

def user_exists(user):
    for sprite in player_group:
        if sprite.name == user:
            return sprite
    return ''

# def get_location(data):
#     return pygame.Vector2(tuple(map(float,data.split(':')[3][1:-1].split(','))))

def return_user_offset(offset,user_location):
    return user_location - offset

def display_players(data,player,level):
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

    
    user_rect = tuple(map(int,data.split(':')[4][6:-2].split(', ')))
    user_rect =  pygame.Rect((user_rect[0],user_rect[1]),(user_rect[2],user_rect[3])) 


    offset.x = player.rect.centerx  - half_width
    offset.y = player.rect.centery  - half_height

    user_offset = user_rect.topleft
    
    animation = player.animations[players[username]["status"]]
    
    # character_path = 'graphics/player/'
    current_user.change_image(animation, players[username]["frame"])
    current_user.location(user_offset)
    temp_group.update()
    
    level.player_sprites.add(current_user)
    level.visible_sprites.add(current_user)

    # for sprite in sorted(player_group.sprites(), key=lambda sprite: sprite.rect.centery):
    #         offset_pos = return_user_offset(offset, user_offset)
    #         display_surface.blit(sprite.image, offset_pos)
 
    temp_group.remove(current_user)
    pass

