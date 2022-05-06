from queue import Empty
import pygame
import boxes
from initial_connection_client import *
pygame.init()
screen = pygame.display.set_mode((1460,920))
base_font = pygame.font.Font(None, 45)


Login_img= pygame.image.load(r'Images/Intro_Images/Login.png').convert()
register_img = pygame.image.load(r'Images/Intro_Images/Register.png')
intro_img= pygame.image.load(r'Images/Intro_Images/374088.jpg').convert()
input_bar =  pygame.Surface((545,68))

login_x = (screen.get_width()-Login_img.get_width())/2
login_y = (screen.get_height()-Login_img.get_height())/2
username_text = ['',]
password_text = ['',]
confirmpassword_text = ['',]
mode = 'login'
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

def display_screen(choice: str) -> dict:

    global login_y
    global login_x

    pygame.display.set_caption('Intro yooo dude so cool!!!!')
    screen.blit(intro_img,(0,0))
    if choice == 'login':
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
    elif choice == 'signup':
        screen.blit(register_img,(login_x,login_y))
        pygame.display.flip() 
        input_list = {  
        "switchlogin" : boxes.input_box(191,41,login_x+10,login_y+10,screen),
        "switchregister" : boxes.input_box(191,41,login_x+299,login_y+10,screen),
        "username" : boxes.input_box(421,35,login_x+40,login_y+143,screen),
        "password" : boxes.input_box(421,35,login_x+40,login_y+243,screen),
        "confirmpassword": boxes.input_box(421,35,login_x+40,login_y+343,screen),
        "cancel" : boxes.input_box(191,41,login_x+10,login_y+450,screen),
        "apply" : boxes.input_box(191,41,login_x+299,login_y+450,screen),
        } 
        pygame.display.flip()

    return input_list



def key_input(input_rect,rect_name):
    global username_text, password_text, confirmpassword_text
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

                if rect_name == "password" or rect_name == "confrimpassword":
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
    init()
    global username_text, password_text, confirmpassword_text,mode
    rect_list = display_screen(mode)
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
                            # password_text[0] = pass_text[0]
                            pygame.display.update()
                    elif rect == "confirmpassword":
                        while not pending:
                            pending = boxes.key_input(rect_list[rect],confirmpassword_text)
                            pass_text[0] = len(confirmpassword_text[0])*'*'
                            boxes.font_render(rect_list[rect],base_font,screen,pass_text,(202,202,202))
                            # confirmpassword_text[0] = pass_text[0]
                            pygame.display.update()
                    elif rect == "switchregister":
                        mode = 'signup'
                        rect_list = display_screen(mode)
                        username_text[0] = ''
                        password_text[0] = ''
                        break
                    elif rect == "switchlogin":
                        mode = 'login'
                        rect_list = display_screen(mode)
                        username_text[0] = ''
                        password_text[0] = ''
                        confirmpassword_text[0] = ''
                        break
                    elif rect == "apply":
                        if mode == 'signup':
                            result = user_connection(mode, username_text[0],password_text[0],confirmpassword_text[0])
                        elif mode == 'login':
                            result = user_connection(mode, username_text[0],password_text[0])
                        if result[0] != "Correct password" and result[0] != "Signup completed":
                            error_box = boxes.input_box(650,35,login_x-75,login_y-100,screen,(202,202,202),255)
                            boxes.font_render(error_box,base_font,screen,["[ ! ] "+result[0],],(202,202,202))
                            pygame.display.update()
                        else:
                            result.pop(0)
                            return result
                    elif rect == "cancel":
                        return
                    else:
                        pending = None

# ------------------------------------------------------------------------

if __name__ == '__main__':
    main()