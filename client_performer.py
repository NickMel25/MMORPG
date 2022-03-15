from tkinter import CENTER
import pygame
from entity import Entity
import __main__
from fake_player import fake_player
import level

players = {}
rect = ''

player = fake_player()
playersg = pygame.sprite.Group()
playersg.add(player)

def append(data):
    print(data)
    temp = ''
    answers = data.split(":")
    info_list = {}
    players[answers[0]]= info_list
    info_list["username"] = answers[0]
    info_list["direction"] = answers[1]
    info_list["attacking"] = answers[2]
    temp = answers[3][1:-1]
    temp =  tuple(map(int, temp.split(',')))
    info_list["location"] = temp
    info_list["hitbox"] = answers[4]
    info_list["connection"] = data[1]

def update(rect,location):
    rect.center = location





def display_players(data):
    global rect
    username = data.split(':')[0]
    


    append(data)
    character_path = 'graphics/player/'
    full_path=character_path+'down_idle/idle_down.png'
    print(full_path)
    

    # hitbox = players[username]["hitbox"]
    # full_path = character_path+players[username]["direction"]
    # rect = image.get_rect(center=hitbox.center)
    print(data)
    
    
    playersg.draw(__main__.game.screen)
    playersg.update(players[username]["location"])
    # player.update_players(players[username]["location"])

#   image = pygame.image.load(full_path)
    
    # rect = image.get_rect()

    

    # pygame.display.update()
    print(rect)
