import pygame
import chat_client
class Chat:

    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.input_rect = self.input_box(10,520,225,20,(0,0,0))
        self.chat_rect = self.input_box(10,290,225,225,(0,0,0))

    def display(self):
        self.screenblit(self.input_rect,self.input_rect.topleft)
        self.screenblit(self.chat_rect,self.chat_rect.topleft)

    def input_box(self,x,y,width,height,color=(255,255,255),image = "none",):
        if image == "none":
            input_rectangle = pygame.Surface((width,height)) 
            input_rectangle.set_alpha(100)
            input_rectangle.fill(color) 
            return self.screenblit(input_rectangle,(x,y))
        else:
            return self.screenblit(image,x,y)

    def screenblit(self,rectangle,position):
        if str(type(rectangle)) == "<class 'pygame.Surface'>": 
            return self.display_surface.blit(rectangle, position )
        else:
            surface = pygame.Surface((rectangle.w,rectangle.h))
            surface.fill((0,0,0))
            surface.set_alpha(100)
            return self.display_surface.blit(surface,position)