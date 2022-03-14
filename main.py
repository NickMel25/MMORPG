import pygame, sys
from player import Player
from settings import *
from level import Level
import udp_client
import threading

class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('MMO Game')
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.player = self.level.return_player()

        # sound
        main_sound = pygame.mixer.Sound('audio/main.ogg')
        main_sound.set_volume(0.5)
        main_sound.play(loops=-1)

    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()
            self.screen.fill(WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)
            ans = Player.to_string(self.player)
            if not ("right_idle" in ans.split(":") or "left_idle" in ans.split(":") or "down_idle" in ans.split(":") or "up_idle" in ans.split(":")):
                udp_client.proccess(Player.to_string(self.player))
            

if __name__ == '__main__':
    game = Game()
    game.run()