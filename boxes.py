import pygame
pygame.init()



def input_box(width,height,x,y,screen,color=(255,255,255),alpha=50,image = "none",):
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



def key_input(input_rect,text):
    while True: 
        for event in pygame.event.get():
            exit(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not collides(input_rect,event):
                    return event
            
            elif event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_RETURN:
                    return event
                elif event.key == pygame.K_BACKSPACE:
                    text[0] = text[0][:-1]
                    return
                else:
                    text[0] += event.unicode
                    return
            
                    

def font_render(input_rect,font,screen,text,color=(255,255,255),alpha=255):
                
 
                text_surface = font.render(text[0], True, (255,255,255))
                
                
                if text_surface.get_width() < input_rect.w:
                    screenblit(input_rect,(input_rect.x,input_rect.y),screen,alpha,color)
                    screenblit(text_surface,(input_rect.x,input_rect.y+3),screen,255,(255,255,255))
                    # pygame.display.update()               
                else:
                    text[0] = text[0][:-1]
