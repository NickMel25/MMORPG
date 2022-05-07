import pygame, sys
from player import Player
from settings import *
from level import Level
# import udp_client
from chat_rect import Chat
import boxes
import intro_screen
import end_conn_client
from connection import Connection

class Game:

    def __init__(self,data,connection):
        # general setup
        global player 

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('U got Hacked')
        self.clock = pygame.time.Clock()
        self.level = Level(data)
        player = self.level.return_player()
        self.connection = connection

    
    def run(self):
        global game
        global player

        self.connection.udp_client.start_thread(player,self.level)
        chat_rect = Chat(self.screen,player.username,self.connection.chat_client)
        chat_rect.thread_start()

        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and boxes.collides(chat_rect.input_rect,event):
                    player.chat_paused = True
                if event.type == pygame.MOUSEBUTTONDOWN and not boxes.collides(chat_rect.input_rect,event):
                    player.chat_paused = False
                if event.type == pygame.QUIT:
                    self.connection.end_conn_client.end_conn()
                    raise Exception("closing all")

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
                        # quit game button
                        if 660 <= mouse[0] <= 740 and 385 <= mouse[1] <= 415:
                            self.connection.end_conn_client.end_conn()
                            raise Exception("closing all")

                        


            self.screen.fill(WATER_COLOR)
            self.level.run()
            chat_rect.display()
            boxes.font_render(chat_rect.input_rect,chat_rect.font,self.screen,chat_rect.insert_text,(0,0,0),100)
            pygame.display.update()
            self.clock.tick(FPS)
            ans = player.to_string()
            self.connection.udp_client.send(ans)


def main():
    try: 
        connection = Connection()
        data = intro_screen.main(connection.init_conn_client)
        connection.chat_client.connect()
        game = Game(data,connection)
        game.run()
    finally:
        try:
            connection.close_con()
        except UnboundLocalError:
            pass
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    main()
