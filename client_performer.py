import pygame
from fake_player import fake_player


class Client_performer:

    def __init__(self) -> None:
        self.players = {}
        self.rect = ''
        self.player_stats = ''
        self.player_group = pygame.sprite.Group()
        self.temp_group = pygame.sprite.Group()
        self.offset = pygame.math.Vector2()
        self.level = ''


    def set_level(self,level):
        self.level = level


    def append(self,data):
        print(data)
        temp = ''
        answers = data.split(":")
        info_list = {}
        self.players[answers[0]]= info_list
        info_list["username"] = answers[0]
        info_list["status"] = answers[1]
        info_list["attacking"] = answers[2]
        temp = answers[3][1:-1]
        temp =  tuple(map(int, temp.split(',')))
        info_list["location"] = temp
        info_list["hitbox"] = answers[4]
        info_list["frame"] = answers[5]
        info_list["connection"] = data[1]


    def user_exists(self,user):
        for sprite in self.player_group:
            if sprite.name == user:
                return sprite
        return ''


    def display_players(self,data,player,level):
        global rect
        
        self.append(data)
        username = data.split(':')[0]
        display_surface = pygame.display.get_surface()
        half_width = display_surface.get_size()[0] // 2
        half_height = display_surface.get_size()[1] // 2

        # prepares and adds the fake player to a group
        current_user = self.user_exists(username)
        if '' == current_user:
            current_user = fake_player(username)
            self.player_group.add(current_user)
        self.temp_group.add(current_user)
    
        user_rect = tuple(map(int,data.split(':')[4][6:-2].split(', ')))
        user_rect =  pygame.Rect((user_rect[0],user_rect[1]),(user_rect[2],user_rect[3])) 
        self.offset.x = player.rect.centerx  - half_width
        self.offset.y = player.rect.centery  - half_height

        user_offset = user_rect.topleft
        animation = player.animations[self.players[username]["status"]]
        
        # character_path = 'graphics/player/'
        current_user.change_image(animation, self.players[username]["frame"])
        current_user.location(user_offset)
        self.temp_group.update()
        
        level.player_sprites.add(current_user)
        level.visible_sprites.add(current_user) 
        self.temp_group.remove(current_user)


def update(rect,location):
        rect.center = location


def return_user_offset(offset,user_location):
    return user_location - offset