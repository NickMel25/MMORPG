import pygame
class fake_player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load('graphics/player/down_idle/idle_down.png')
        self.rect = self.image.get_rect()

    
    def update(self,location):
        self.rect.center = location