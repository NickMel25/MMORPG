import pygame
import boxes
import threading


class Chat:

    def __init__(self,screen,username,chat_client):


        self.screen = screen
        self.display_surface = pygame.display.get_surface()
        self.input_rect = boxes.input_box(300,20,10,520,self.screen,(0,0,0),100)
        self.chat_rect = boxes.input_box(300,300,10,215,self.screen,(0,0,0),100)
        self.level = ''
        self.font = pygame.font.Font(None, 20)
        self.insert_text = ['',]
        self.chat_log = ['']*15
        self.username = username
        self.chat_client = chat_client

    def shift_append(self,msg):
        for i in range(len(self.chat_log)-1):
            self.chat_log[i] = self.chat_log[i+1]
        self.chat_log[len(self.chat_log)-1] = msg
        print(self.chat_log[len(self.chat_log)-1])
        return

     

    def display(self):
        boxes.screenblit(self.input_rect,self.input_rect.topleft,self.screen,100,(0,0,0))
        boxes.screenblit(self.chat_rect,self.chat_rect.topleft,self.screen,100,(0,0,0))

        i = 0
        for log in self.chat_log:
            text_surface = self.font.render(log, True, (255,255,255))
            boxes.screenblit(text_surface,(self.chat_rect.x,self.chat_rect.y+3+i),self.screen,255,(255,255,255))
            i+=20
            
            # if text_surface.get_width() < self.input_rect.w:
            #     boxes.screenblit(self.input_rect,(self.input_rect.x,self.input_rect.y),self.screen,100,(0,0,0))
            #     boxes.screenblit(text_surface,(self.input_rect.x,self.input_rect.y+3),self.screen,255,(255,255,255))

        pygame.display.update()
        pass


    def sort_text(self,text):
            temp = ''
            text_surface = self.font.render(text[0], True, (255,255,255))
            completed = False
            while not completed:
                while text_surface.get_width() > self.input_rect.w:
                    temp += text[0][-1]
                    text[0] = text[0][:-1]
                    text_surface = self.font.render(text[0], True, (255,255,255))
                self.shift_append(text[0])
                print(temp)
                text[0] = temp[::-1]
                if temp == '':
                    break
                temp = ''

            

    def recv_chat(self):
        msg = ['']
        while True:
            msg[0] = self.chat_client.recv()

            
            self.sort_text(msg)
            self.display()


    def send_text(self,text):
        self.chat_client.send_message(text[0])
        self.insert_text[0] = ''


    def thread_start(self):
        thread = threading.Thread(target=self.recv_chat)
        thread.daemon = True
        thread.start()
    


    def get_events(self,main_events):
        self.events.append(main_events)

