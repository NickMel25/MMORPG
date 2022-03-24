import pygame
from queue import Empty

def input_box(width,height,x,y,screen,color=(255,255,255),alpha=0,image = "none",):
    if image == "none":
        input_rectangle = pygame.Surface((width,height)) 
        input_rectangle.set_alpha(alpha)
        input_rectangle.fill(color) 
        return screenblit(input_rectangle,(x,y),screen,alpha,color)
    else:
        return screenblit(image,(x,y),screen,alpha)

def screenblit(rectangle,position,screen,alpha, color):
    if str(type(rectangle)) == "<class 'pygame.Surface'>": 
        return screen.blit(rectangle, position)
    else:
        surface = pygame.Surface((rectangle.w,rectangle.h))
        surface.fill(color)
        surface.set_alpha(alpha)
        return screen.blit(surface,position)
        
def exit(event):
    if event.type == pygame.QUIT:
        pygame.quit()


def collides(input_rect, event):
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and input_rect.collidepoint(event.pos)

def key_input(input_rect,rect_name):
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
                    boxes.screenblit(input_rect,(input_rect.x,input_rect.y),screen,255,(202,202,202))
                    boxes.screenblit(text_surface,(input_rect.x,input_rect.y+3),screen,255,(202,202,202))
                
                    if rect_name == "username":
                        username_text = text
                    elif rect_name == "password":
                        password_text = text
                
                    pygame.display.update()
                
                else:
                    text = text[:-1]