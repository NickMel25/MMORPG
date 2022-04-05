import pygame
class fake_player(pygame.sprite.Sprite):
    def __init__(self, name) -> None:
        super().__init__()
        self.image = pygame.image.load('graphics/player/down_idle/idle_down.png')
        self.rect = self.image.get_rect()
        self.name = name
        self.next_location = (0,0)
        self.image_path = ''
    
    def change_image(self,animation,frame):
        self.image_path = animation[int(frame)]

    def location(self,location):
        self.next_location = location

    def update(self):
        self.rect.topleft = self.next_location
        # self.image = pygame.image.load(self.image_path)
        self.image = self.image_path