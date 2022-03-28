from queue import Empty
import pygame
import boxes

pygame.init()
screen = pygame.display.set_mode((1460,920))
base_font = pygame.font.Font(None, 45)


Login_img= pygame.image.load(r'Images/Intro_Images/Login.png').convert()
intro_img= pygame.image.load(r'Images/Intro_Images/374088.jpg').convert()
input_bar =  pygame.Surface((545,68))

login_x = (screen.get_width()-Login_img.get_width())/2
login_y = (screen.get_height()-Login_img.get_height())/2
username_text = ['',]
password_text = ['',]

def screenblit(rectangle,x,y):
    if str(type(rectangle)) == "<class 'pygame.Surface'>": 
        return screen.blit(rectangle, (x,y))
    else:
        surface = pygame.Surface((rectangle.w,rectangle.h))
        surface.fill((202,202,202))
        return screen.blit(surface,(x,y))


# ------------------------------------------------------------------------

def exit(event):
    if event.type == pygame.QUIT:
        pygame.quit()


# ------------------------------------------------------------------------

def display_screen():

    global login_y
    global login_x


    pygame.display.set_caption('Intro yooo dude so cool!!!!')
    screen.blit(intro_img,(0,0))

    screen.blit(Login_img,(login_x,login_y))
    pygame.display.flip() 
    input_list = {  
    "switchlogin" : boxes.input_box(191,41,login_x+10,login_y+10,screen),
    "switchregister" : boxes.input_box(191,41,login_x+299,login_y+10,screen),
    "username" : boxes.input_box(421,35,login_x+40,login_y+143,screen),
    "password" : boxes.input_box(421,35,login_x+40,login_y+286,screen),
    "cancel" : boxes.input_box(191,41,login_x+10,login_y+450,screen),
    "apply" : boxes.input_box(191,41,login_x+299,login_y+450,screen),
    } 
    pygame.display.flip()

    return input_list


def key_input(input_rect,rect_name):
    global username_text
    global password_text
    if rect_name == "username":
        text = username_text[0]
    elif rect_name == "password":
        text = password_text[0]
    while True:
        for event in pygame.event.get():
            exit(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not boxes.collides(input_rect,event):
                    return event
            
            elif event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_RETURN:
                    return Empty
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

                if rect_name == "password":
                    pass_text = len(text)*'*'
                else:
                    pass_text = text
                text_surface = base_font.render(pass_text, True, (255, 255, 255))
                print(text_surface.get_width())
                
                
                if text_surface.get_width() < input_rect.w:
                    boxes.screenblit(input_rect,(input_rect.x,input_rect.y),screen,255,(202,202,202))
                    boxes.screenblit(text_surface,(input_rect.x,input_rect.y+3),screen,255,(202,202,202))
                
                    if rect_name == "username":
                        username_text[0] = text
                    elif rect_name == "password":
                        password_text[0] = text
                
                    pygame.display.update()
                
                else:
                    text = text[:-1]
                    return event

# ------------------------------------------------------------------------

def main():
    global username_text, password_text
    rect_list = display_screen()
    print(type(rect_list["switchlogin"]))
    print(type(rect_list["username"]))
    print(type(pygame.surface))
    pending = None
    pass_text = ['',]
    while True:
        for event in pygame.event.get():
            exit(event)
            if pending != None:
                event = pending
                pending = None
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("lolusuck")
            for rect in rect_list:
                if boxes.collides(rect_list[rect], event):
                    if rect == "username":
                        while not pending:
                            pending = boxes.key_input(rect_list[rect],username_text)
                            boxes.font_render(rect_list[rect],base_font,screen,username_text,(202,202,202))
                            pygame.display.update()
                    elif rect == "password":
                        while not pending:
                            pending = boxes.key_input(rect_list[rect],password_text)
                            pass_text[0] = len(password_text[0])*'*'
                            boxes.font_render(rect_list[rect],base_font,screen,pass_text,(202,202,202))
                            password_text[0] = pass_text[0]
                            pygame.display.update()

                    elif rect == "apply":
                        print("we need to connect this to the game")
                        return username_text[0]
                    else:
                        pending = None

# ------------------------------------------------------------------------
