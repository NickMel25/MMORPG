import pygame, sys
from player import Player
from settings import *
from level import Level
import udp_client


game = ''


class Game:
    player = ''

    def __init__(self):
        # general setup
        global player 

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('MMO Game')
        self.clock = pygame.time.Clock()
        self.level = Level()
        player = self.level.return_player()

    def run(self):
        global game
        global player
        udp_client.start_thread(player, self.level)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.level.game_over:
                        mouse = pygame.mouse.get_pos()
                        # restart game button
                        if 540 <= mouse[0] <= 620 and 385 <= mouse[1] <= 415:
                            game = Game()
                            game.run()
                        # quit game button
                        if 660 <= mouse[0] <= 740 and 385 <= mouse[1] <= 415:
                            pygame.quit()
                            sys.exit()

            self.screen.fill(WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)
            ans = player.to_string()
            udp_client.send(ans)


def main():
    global game
    global player_stats
    
    game = Game()
    # player_stats = player.to_string() 
    game.run()


if __name__ == '__main__':
    main()
