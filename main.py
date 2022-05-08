import pygame, sys
import level
from player import Player
from settings import *
from level import Level
import udp_client
from chat_rect import Chat
import boxes

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

        pygame.mouse.set_visible(True)
        global game
        global player

        udp_client.start_thread(player, self.level)
        chat_rect = Chat(self.screen, player.username)
        chat_rect.thread_start(self.level)

        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and boxes.collides(chat_rect.input_rect,event):
                    player.chat_paused = True
                if event.type == pygame.MOUSEBUTTONDOWN and not boxes.collides(chat_rect.input_rect,event) and not self.level.game_over:
                    player.chat_paused = False

                    level.Level.path_found(self.level, pygame.mouse.get_pos())

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if player.chat_paused == True:
                        if player.chat_paused == True and event.key == pygame.K_BACKSPACE:
                            chat_rect.insert_text[0] = chat_rect.insert_text[0][:-1]

                        elif player.chat_paused == True and event.key == pygame.K_RETURN:
                            player.chat_paused = False
                            chat_rect.send_text(chat_rect.insert_text)

                        elif not (event.type == pygame.K_DOWN and event.type == pygame.K_UP and event.type == pygame.K_LEFT and event.type == pygame.K_RIGHT) and player.chat_paused == True:
                            chat_rect.insert_text[0] += event.unicode

                    elif event.key == pygame.K_m:
                        self.level.toggle_menu()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.level.game_over:
                        mouse = pygame.mouse.get_pos()

                        # restart game button
                        if 540 <= mouse[0] <= 620 and 385 <= mouse[1] <= 415:
                            self.level.game_over = False
                            level.Level.restart(self.level)

                        # quit game button
                        if 660 <= mouse[0] <= 740 and 385 <= mouse[1] <= 415:
                            pygame.quit()
                            sys.exit()

            self.screen.fill(WATER_COLOR)
            self.level.run()
            chat_rect.display()
            boxes.font_render(chat_rect.input_rect, chat_rect.font, self.screen, chat_rect.insert_text, (0, 0, 0), 100)
            pygame.display.update()
            self.clock.tick(FPS)
            ans = player.to_string()
            udp_client.send(ans)


def main():
    global game
    
    game = Game()
    # player_stats = player.to_string() 
    game.run()


if __name__ == '__main__':
    main()
