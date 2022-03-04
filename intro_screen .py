from queue import Empty
import pygame

pygame.init()
screen = pygame.display.set_mode((1460,920))
base_font = pygame.font.Font(None, 45)

# input_bar = pygame.image.load(r'Images/Intro_Images/inputbar.jpeg').convert()
Login_img= pygame.image.load(r'Images/Intro_Images/Login.png').convert()
intro_img= pygame.image.load(r'Images/Intro_Images/374088.jpg').convert()
input_bar =  pygame.Surface((545,68))

login_x = (screen.get_width()-Login_img.get_width())/2
login_y = (screen.get_height()-Login_img.get_height())/2
username_text = ''
password_text = ''

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
    "switchlogin" : input_box(191,41,login_x+10,login_y+10),
    "switchregister" : input_box(191,41,login_x+299,login_y+10),
    "username" : input_box(421,35,login_x+40,login_y+143),
    "password" : input_box(421,35,login_x+40,login_y+286),
    "apply" : input_box(191,41,login_x+10,login_y+450),
    "cancel" : input_box(191,41,login_x+299,login_y+450),
    } 
    pygame.display.flip()

    return input_list

# ------------------------------------------------------------------------
    
def input_box(width,height,x,y, image = "none"):
    if image == "none":
        input_rectangle = pygame. Surface((width,height)) 
        input_rectangle. set_alpha(100)
        input_rectangle. fill((255,255,255)) 
        return screenblit(input_rectangle,x,y)
    else:
        return screenblit(image,x,y)

# ------------------------------------------------------------------------

def screenblit(rectangle,x,y):
    if str(type(rectangle)) == "<class 'pygame.Surface'>": 
        return screen.blit(rectangle, (x,y))
    else:
        surface = pygame.Surface((rectangle.w,rectangle.h))
        surface.fill((202,202,202))
        return screen.blit(surface,(x,y))

# ------------------------------------------------------------------------

def collides(input_rect, event):
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and input_rect.collidepoint(event.pos)

# ------------------------------------------------------------------------

def key_input(input_rect,rect_name):
    global username_text
    global password_text
    if rect_name == "username":
        text = username_text
    elif rect_name == "password":
        text = password_text
    while True:
        for event in pygame.event.get():
            exit(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not collides(input_rect,event):
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
                    screenblit(input_rect,input_rect.x,input_rect.y)
                    screenblit(text_surface,input_rect.x,input_rect.y+3)
                
                    if rect_name == "username":
                        username_text = text
                    elif rect_name == "password":
                        password_text = text
                
                    pygame.display.update()
                
                else:
                    text = text[:-1]


# ------------------------------------------------------------------------

def main():
    
    rect_list = display_screen()
    print(type(rect_list["switchlogin"]))
    print(type(rect_list["username"]))
    print(type(pygame.surface))
    pending = Empty
    while True:
        for event in pygame.event.get():
            exit(event)
            if pending != Empty:
                event = pending
            for rect in rect_list:
                if collides(rect_list[rect], event):
                    if rect == "username" or rect == "password":
                        pending = key_input(rect_list[rect],rect)
                    elif rect == "apply":
                        print("we need to connect this to the game")

# ------------------------------------------------------------------------

if __name__ == '__main__':
    main()