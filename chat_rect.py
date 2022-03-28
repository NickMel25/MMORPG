from time import sleep
import pygame
import chat_client
import boxes
import threading

from level import Level

class Chat:

    def __init__(self,screen):
        self.screen = screen
        self.display_surface = pygame.display.get_surface()
        self.input_rect = boxes.input_box(225,20,10,520,self.screen,(0,0,0),100)
        self.chat_rect = boxes.input_box(225,225,10,290,self.screen,(0,0,0),100)
        self.level = ''
        self.font = pygame.font.Font(None, 20)
        self.insert_text = ['',]
        self.chat_log = []


    def display(self):
        boxes.screenblit(self.input_rect,self.input_rect.topleft,self.screen,100,(0,0,0))
        boxes.screenblit(self.chat_rect,self.chat_rect.topleft,self.screen,100,(0,0,0))

    def text_insert(self, event):
        self.insert_text[0] += event.unicode
        boxes.font_render(self.input_rect,self.font,self.screen,self.insert_text,(0,0,0),100)
        self.level.player.chat_paused = False


    def thread_start(self,level):
        self.level = level
        thread = threading.Thread(target=self.text_insert)
        thread.daemon = True
        thread.start()
    
    def get_events(self,main_events):
        self.events.append(main_events)

