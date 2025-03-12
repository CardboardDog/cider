import pygame
def init():
    pygame.init()
    pygame.font.init()
class Gui:
    Open = True
    Input = 0
    Select = False
    Back = False
    Keyboard = ''
    Delete = False
    def __init__(self):
        self.Open = True
        self.Window = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.w,self.h = pygame.display.get_surface().get_size()
        self.Size = 12#int(self.h/25)
        print("display size: ("+str(self.w)+","+str(self.h)+")")
        self.Font = pygame.font.SysFont("hack",self.Size)
    def Clear(self):
        self.Window.fill((0,0,0))
    def Update(self):
        pygame.display.flip()
        self.Input = 0 
        self.Select = False
        self.Back = False
        self.Keyboard = ""
        self.Delete = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Open = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.Input = -1
                elif event.key == pygame.K_DOWN:
                    self.Input = 1
                elif event.key == pygame.K_RETURN:
                    self.Select = True
                elif event.key == pygame.K_ESCAPE:
                    self.Back = True
                elif event.key == pygame.K_BACKSPACE:
                    self.Delete = True
                else:
                    self.Keyboard += event.unicode
    def DrawText(self,text,pos,act):
        surf = self.Font.render(text,True,((0,0,0) if act else (255,255,255)))
        newpos = (pos[0],pos[1]*self.Size)
        if(act):
            bg = surf.get_rect()
            bg.x = newpos[0]
            bg.y = newpos[1]
            pygame.draw.rect(self.Window,(255,255,255),bg)
        self.Window.blit(surf,newpos)
    def DrawEntry(self,text,pos,act):
        surf = self.Font.render(text,True,((0,0,0) if act else (255,255,255)))
        newpos = (pos[0],pos[1]*self.Size)
        if(act):
            bg = surf.get_rect()
            bg.x = newpos[0]
            bg.y = newpos[1]
            pygame.draw.rect(self.Window,(255,255,255),bg)
        self.Window.blit(surf,newpos)
        if(act):
            if(self.Delete):
                return text[:-1]
            return text+self.Keyboard
        return text
def Quit():
    pygame.quit()

