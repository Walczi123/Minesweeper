from random import randrange
import pygame, sys
from pygame.locals import *
from math import ceil, floor

# # # NOT TO CHANGE # # #
__FPS__ = 30  # Frames Per second
__AMOUNT_OF_FIELDS__=(8,8) # Numbers of bombs at row, at column
__BUTTON_SIZE__=(30,30) #Size of button without perimeter
__PERCENTAGE_OF_BOMBS__=(12,18) # (x,y) x-lower bound of percentage of all fields of bombs, y - upper bound
__FONT__='freesansbold.ttf' #Font of number in field
__FONT_SIZE__=int(0.75*__BUTTON_SIZE__[1]) #Size of number in field

def data_update():
    global __BORDER__,__PERIMETER__,__TOOLBAR_SIZE__,__WINDOW_SIZE__,__AMOUNT_OF_NON_BOMBS__,__UNCOVERED_FIELDS__
    __BORDER__=((0.25*__BUTTON_SIZE__[0])/2,(0.25*__BUTTON_SIZE__[1])/2)  #Perimeter of button
    __PERIMETER__=((0.1*__BUTTON_SIZE__[0])//2,(0.1*__BUTTON_SIZE__[1])//2) #Perimeter of window
    __TOOLBAR_SIZE__=(int(__AMOUNT_OF_FIELDS__[0]*__BUTTON_SIZE__[0]+__PERIMETER__[0]*4),35) #Size of toolbar
    __WINDOW_SIZE__=(__TOOLBAR_SIZE__[0],int(__AMOUNT_OF_FIELDS__[1]*__BUTTON_SIZE__[1]+__PERIMETER__[1]*4)+__TOOLBAR_SIZE__[1]) #Size of widows    
    __AMOUNT_OF_NON_BOMBS__=(__AMOUNT_OF_FIELDS__[0])*(__AMOUNT_OF_FIELDS__[1]) #Amount of fields without bombs
    __UNCOVERED_FIELDS__=0 #Number of uncovered fields
    __AMOUNT_OF_BOMBS__=0 #Amount of bombs, changed after addition of bombs
    
def mantissa(x):
    return x-floor(x)

class Button:
    """
    bool bomb - True if in object Button is a bomb, False otherwise
    int number - Amount of bombs in adjacent fields ,default = 0
    bool flag - True if in object Button is a flag, False otherwise
    bool uncovered - False if object is covered, True otherwise
    """
    bomb=False
    number=0
    flag=False
    uncovered=False

    def __init__(
        self, 
        bomb=False,
        number=0,
        flag=False, 
        uncovered=False,
                 ): 
        if type(bomb)is not bool : bomb = False
        if type(number)is not int : number = 0
        if type(flag)is not bool : flag = False
        if type(flag)is not bool : uncovered = False
        self.bomb=bomb
        self.number=number
        self.flag=flag
        self.uncovered=uncovered
    def change_cover(self):
        self.uncovered=True
        global __UNCOVERED_FIELDS__
        __UNCOVERED_FIELDS__+=1


def bomb_around(board=None,y=-1,x=-1):
    if board==None or y==-1 or x==-1: return
    for i in range(0,3):
        for j in range(0,3):
           if x-1+i>=0 and y-1+j>=0 and x-1+i<__AMOUNT_OF_FIELDS__[1] and y-1+j<__AMOUNT_OF_FIELDS__[0]:
               if board[y-1+j][x-1+i].bomb and (i,j)!=(1,1) :                   
                   board[y][x].number+=1

def random_bombs(board=None):  
    if board==None: return
    global __AMOUNT_OF_NON_BOMBS__,__AMOUNT_OF_BOMBS__,__AMOUNT_OF_FIELDS__
    __AMOUNT_OF_BOMBS__=int(randrange(__PERCENTAGE_OF_BOMBS__[0],__PERCENTAGE_OF_BOMBS__[1])*(__AMOUNT_OF_NON_BOMBS__/100))
    __AMOUNT_OF_NON_BOMBS__-=__AMOUNT_OF_BOMBS__
    for i in range(0,__AMOUNT_OF_BOMBS__):
        y=randrange(0,__AMOUNT_OF_FIELDS__[0])
        x=randrange(0,__AMOUNT_OF_FIELDS__[1])
        if board[y][x].bomb == False:
            board[y][x].bomb = True
        else:
            i=i-1
    for i in range(0,__AMOUNT_OF_FIELDS__[0]) :
         for j in range(0,__AMOUNT_OF_FIELDS__[1]):
             if not board[i][j].bomb : bomb_around(board,i,j)

def message_display(text,y,x,surface,color,font,font_size):
    text_font = pygame.font.Font(font,font_size)
    text_face=text_font.render(text, True, color)
    text_surface, text_rectangle = text_face, text_face.get_rect()
    text_rectangle.center = (x,y)
    surface.blit(text_surface, text_rectangle)

def display_number(number,y,x,surface):
    colors_table=[]
    colors_table.append((2,98,214))     #1
    colors_table.append((1,120,37))     #2
    colors_table.append((116,3,3))      #3
    colors_table.append((0,0,64))       #4
    colors_table.append((255,0,0))      #5
    colors_table.append((131,14,122))   #6
    colors_table.append((75,7,70))      #7
    colors_table.append((128,0,64))     #8
    message_display(str(number),y,x,surface,colors_table[number-1],__FONT__,__FONT_SIZE__)

def draw(surface=None, board=None):
    if board==None or surface==None: return
    GROUND_COLOR = (30, 30, 30)
    BUTTON_COV = (200,200,200)
    BUTTON_UNCOV = (150,150,150)
    BUTTON_FLAG = (255,249,0)
    BUTTON_BOMB = (193,0,0)
    ground = (
        0, 0,
        __WINDOW_SIZE__[0],__WINDOW_SIZE__[1]
    )
    pygame.draw.rect(surface, GROUND_COLOR, ground)    
    for i in range(0,__AMOUNT_OF_FIELDS__[0]):
        for j in range(0,__AMOUNT_OF_FIELDS__[1]):                     
            position = (
                __PERIMETER__[0]+__BORDER__[0]+__BUTTON_SIZE__[0]*i,__TOOLBAR_SIZE__[1]+__PERIMETER__[1]+__BORDER__[1]+__BUTTON_SIZE__[1]*j, 
                __BUTTON_SIZE__[0]-__BORDER__[0],__BUTTON_SIZE__[1]-__BORDER__[1]
            )
            BUTTON_COLOR=BUTTON_COV
            if board[i][j].flag==True :
                BUTTON_COLOR=BUTTON_FLAG
            if board[i][j].uncovered==True:
                if board[i][j].bomb==True:
                    BUTTON_COLOR=BUTTON_BOMB 
                else:
                    BUTTON_COLOR=BUTTON_UNCOV
            pygame.draw.rect(surface, BUTTON_COLOR, position)
            if board[i][j].uncovered==True and board[i][j].number != 0:
                display_number(board[i][j].number,position[1]+position[3]/2,position[0]+position[2]/2,surface)
                
def position_to_button(pos=None):
    if pos == None : return
    button_pos=((pos[0]-__PERIMETER__[0])/__BUTTON_SIZE__[0],(pos[1]-__PERIMETER__[1]-__TOOLBAR_SIZE__[1])/__BUTTON_SIZE__[1])
    t=False
    #if |floor(button(x))-center_of_buttron(x))| <= (center_of_buttron(x)-border(x)) and |floor(button(y))-center_of_buttron(y))| <= (center_of_buttron(y)-border(y)):
    if abs((int(mantissa(button_pos[0])*__BUTTON_SIZE__[0])%__BUTTON_SIZE__[0])-__BUTTON_SIZE__[0]/2) <= ((__BUTTON_SIZE__[0]/2)-__BORDER__[0]):
        if abs((int(mantissa(button_pos[1])*__BUTTON_SIZE__[1])%__BUTTON_SIZE__[1])-__BUTTON_SIZE__[1]/2) <= ((__BUTTON_SIZE__[1]/2)-__BORDER__[1]):
            t=True
    button_pos=(ceil(button_pos[0]),ceil(button_pos[1]))
    return (t,button_pos[0]-1,button_pos[1]-1)
     
def Uncoverall(board=None):
    if board==None : return
    for i in range(0,__AMOUNT_OF_FIELDS__[0]):
        for j in range(0,__AMOUNT_OF_FIELDS__[1]):
            if board[i][j].bomb==True:
                board[i][j].uncovered=True

def Uncover_field(board,y,x):
    if board==None or y==-1 or x==-1 or board[y][x].uncovered : return
    global __AMOUNT_OF_FIELDS__
    if board[y][x].uncovered: return
    board[y][x].change_cover() 
    if board[y][x].number == 0 :
        for i in range(0,3):
            for j in range(0,3):
               if x-1+i>=0 and y-1+j>=0 and x-1+i<__AMOUNT_OF_FIELDS__[1] and y-1+j<__AMOUNT_OF_FIELDS__[0]:
                   if (i,j)!=(1,1) :                   
                        Uncover_field(board,y-1+j,x-1+i)

def mouse_at_position(range,test):
    if range[0][0]>=test[0] and range[0][0]<=test[2] and range[0][1]>=test[1] and range[0][1]<=test[3]:
        if range[1][0]>=test[0] and range[1][0]<=test[2] and range[1][1]>=test[1] and range[1][1]<=test[3]:
            return True   
    return False

class THE:
    def __init__(self):
        self.if_end=False
        self.win_lose=False #True - win, False - lose
        self.choosing=False
        self.end_iter=True
    
    def END(self):
        if self.if_end:
            if self.win_lose:
                self.Winning()
            else:
                self.Losing()
    
    def Case_of_win(self):
        global __UNCOVERED_FIELDS__,__AMOUNT_OF_NON_BOMBS__
        if __UNCOVERED_FIELDS__==__AMOUNT_OF_NON_BOMBS__ :      
            self.if_end=True
            self.win_lose=True
            
    def Case_of_lose(self):
        if self.if_end and not self.win_lose :      
            self.if_end=True
            self.win_lose=False 

    def check_end(self,surface,board,toolbar):
        self.Case_of_win()
        self.Case_of_lose()
        if self.if_end :
            Uncoverall(board)
            draw(surface,board)
            toolbar.draw()
            if self.end_iter:
                pygame.time.wait(1000)
                self.end_iter = not self.end_iter
            if self.win_lose:
                self.Winning(surface)
            else:
                self.Losing(surface)
    
    def draw_options(self,surface):       
        self.button_position=[]
        rec=(__WINDOW_SIZE__[0]/2 -100 , __WINDOW_SIZE__[1]/2 + 20, 95, 30)
        pygame.draw.rect(surface, (150,150,150), rec)
        rec=(__WINDOW_SIZE__[0]/2 -97 , __WINDOW_SIZE__[1]/2 + 23, 89, 24)
        self.button_position.append((rec[0],rec[1],rec[0]+rec[2],rec[1]+rec[3]))
        pygame.draw.rect(surface, (230,230,230), rec)
        rec=(__WINDOW_SIZE__[0]/2 +5 , __WINDOW_SIZE__[1]/2 + 20, 95, 30)
        pygame.draw.rect(surface, (150,150,150), rec)
        rec=(__WINDOW_SIZE__[0]/2 +8 , __WINDOW_SIZE__[1]/2 + 23, 89, 24)
        self.button_position.append((rec[0],rec[1],rec[0]+rec[2],rec[1]+rec[3]))
        pygame.draw.rect(surface, (230,230,230), rec)
        message_display("Try Again",__WINDOW_SIZE__[1]/2 + 35,__WINDOW_SIZE__[0]/2-50,surface,(0,0,0),__FONT__,15)
        message_display("Exit",__WINDOW_SIZE__[1]/2 + 35,__WINDOW_SIZE__[0]/2+50,surface,(0,0,0),__FONT__,15)
        self.choosing=True

    def Winning(self,surface):
        rec=(__WINDOW_SIZE__[0]/2 -115, __WINDOW_SIZE__[1]/2 - 55, 230, 120)
        pygame.draw.rect(surface, (0,150,0), rec)
        rec=(__WINDOW_SIZE__[0]/2 -110, __WINDOW_SIZE__[1]/2 - 50, 220, 110)
        pygame.draw.rect(surface, (255,255,255), rec)
        message_display("You Win !!!",__WINDOW_SIZE__[1]/2 -10,__WINDOW_SIZE__[0]/2,surface,(0,0,0),__FONT__,30)   
        self.draw_options(surface)  

    def Losing(self,surface):
        rec=(__WINDOW_SIZE__[0]/2 -115, __WINDOW_SIZE__[1]/2 - 55, 230, 120)
        pygame.draw.rect(surface, (255,0,0), rec)
        rec=(__WINDOW_SIZE__[0]/2 -110, __WINDOW_SIZE__[1]/2 - 50, 220, 110)
        pygame.draw.rect(surface, (255,255,255), rec)
        message_display("You Fail !!!",__WINDOW_SIZE__[1]/2 -10,__WINDOW_SIZE__[0]/2,surface,(0,0,0),__FONT__,30)
        self.draw_options(surface)

    def last_will(self,pos):
        if mouse_at_position(pos,self.button_position[0]):
            pygame.quit()
            run_game()
        elif mouse_at_position(pos,self.button_position[1]):
            pygame.quit()
            sys.exit()

def Button_click(input=None, board=None, button=None):
    if board==None or input==None or button==None: return
    t,y,x = input
    if t:   
        if button == 1: #left click => uncover or bomb
            if board[y][x].flag!=True:
                if board[y][x].bomb==True:
                    return True
                if board[y][x].uncovered==False:
                    Uncover_field(board,y,x)
        elif button == 3: #right click => flag          
            board[y][x].flag = not board[y][x].flag
    return False

def change_board_size(x):
    global __AMOUNT_OF_FIELDS__
    __AMOUNT_OF_FIELDS__=(x[0],x[1])
    pygame.quit()
    run_game()

def change_percentage_of_bombs(x):
    global __PERCENTAGE_OF_BOMBS__
    __PERCENTAGE_OF_BOMBS__=(x[0],x[1])
    pygame.quit()
    run_game()

class Menu:
    def __init__(self, position,color,width,screen):
        self.options=[]
        self.options_fields=[]
        self.width=width
        self.font_size=25
        self.frame=2
        self.height=((self.font_size+2*self.frame)*len(self.options))+max((len(self.options)-1)*self.frame,0)
        self.image = pygame.Surface((self.width, self.height))
        self.color=color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.position=position
        self.rect.topleft = self.position
        self.screen=screen
    def add_options(self, *args):
        y=0
        x,=args
        for i in x:
            if y<len(i[0]):y=len(i[0])
            self.options.append(i)       
        self.width=max(y*12+20,self.width)
        self.height=((self.font_size+2*self.frame)*len(self.options))+max((len(self.options)-1)*self.frame,0)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
        self.options_fields=[]
    def sub_draw(self):       
        opt = len(self.options)
        if opt>0:
            image_1 = pygame.Surface((self.width-2*self.frame, max(0,self.height-2*self.frame)))
            image_1.fill((200,200,200))
            rect_1 = image_1.get_rect()
            rect_1.topleft = (self.rect.topleft[0]+self.frame,self.rect.topleft[1]+self.frame)
            self.screen.blit(self.image, self.rect)
            self.screen.blit(image_1, rect_1)
            if opt > 1 :
                image_2 = pygame.Surface((self.width-12*self.frame, self.frame))
                image_2.fill(self.color)
                rect_2 = image_2.get_rect()
                for i in range(opt):
                    rect_2.topleft =(self.rect.topleft[0]+6*self.frame,self.rect.topleft[1]+i*self.font_size+self.frame*int(i*2.5))
                    self.screen.blit(image_2, rect_2)
    def draw(self):
        self.sub_draw()
        for x in enumerate(self.options):
            message_display(x[1][0],self.rect.topleft[1]+self.frame*8+x[0]*self.font_size+int(x[0]*2.5)*self.frame,self.rect.topleft[0]+self.frame+self.width/2,self.screen,(0,0,0),__FONT__,self.font_size-10)
    def in_range(self,pos):
        s=(self.rect.topleft[0]+self.frame,self.rect.topleft[1]+self.frame,
                self.rect.topleft[0]+self.width-self.frame,self.rect.topleft[1]+self.height-self.frame)
        self.options_fields=[]
        opt=len(self.options)
        for x in range(opt):
            y=(self.rect.topleft[0]+self.frame,self.rect.topleft[1]+self.frame+x*(self.height-self.frame)/opt,
                self.rect.topleft[0]+self.width-self.frame,self.rect.topleft[1]+(x+1)*(self.height-self.frame)/opt)
            self.options_fields.append(y)
        return mouse_at_position(pos,s)
    def action(self,pos):
        for x in enumerate(self.options_fields):
            if mouse_at_position(pos,x[1]):
                self.options[x[0]][1](self.options[x[0]][2])                 

class ToolBar_Button:
    def __init__(self, position,width, height,text,screen,*args):
        self.image = pygame.Surface((width, height))
        self.width=width
        self.height=height
        self.color=((220,220,220))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.text=text
        self.text_position=(position[0]+width/2,position[1]+2+height/2)
        self.font_size=height-8
        self.screen=screen
        self.frame=2
        self.menu=Menu((position[0]+self.frame,position[1]+height-2*self.frame),(150,150,150),self.width-2*self.frame,screen)
        self.menu.add_options(args)
        self.menu_open=False
    def draw_subbuton(self):
        image_1 = pygame.Surface((self.width-2*self.frame, self.height-2*self.frame))
        image_1.fill((150,150,150))
        rect_1 = image_1.get_rect()
        rect_1.topleft = (self.rect.topleft[0]+self.frame,self.rect.topleft[1]+self.frame)
        image_2 = pygame.Surface((self.width-4*self.frame, self.height-4*self.frame))
        image_2.fill(self.color)
        rect_2 = image_2.get_rect()
        rect_2.topleft =(self.rect.topleft[0]+2*self.frame,self.rect.topleft[1]+2*self.frame)
        self.screen.blit(self.image, self.rect)
        self.screen.blit(image_1, rect_1)
        self.screen.blit(image_2, rect_2)
    def draw(self):
        self.draw_subbuton()
        message_display(self.text,self.text_position[1],self.text_position[0],self.screen,(0,0,0),__FONT__,self.font_size)
        if self.menu_open : self.menu.draw()
    def position(self):
        res=(self.rect.topleft[0]+self.frame,self.rect.topleft[1]+self.frame,
             self.rect.topleft[0]+self.width-self.frame,self.rect.topleft[1]+self.height-self.frame)
        return res
    def click(self):
        self.menu_open= not self.menu_open

class Toolbar:
    def __init__(self, width, height,screen):
        self.image = pygame.Surface((width, height))
        self.width=width
        self.height=height
        self.color=((250,250,250))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)
        self.screen=screen
        self.leftbutton = ToolBar_Button((6,6),min(width/3,50),height-12,"Size",screen,("8x8",change_board_size,(8,8)),("16x16",change_board_size,(16,16)),("30x16",change_board_size,(30,16)))
        self.rightbutton = ToolBar_Button((11+min(width/3,50),6),min(width/3,60),height-12,"Mines",screen,("low amount",change_percentage_of_bombs,(6,12)),("medium amount",change_percentage_of_bombs,(12,18)),("hight amount",change_percentage_of_bombs,(18,25)))

    def sub_draw(self):
        frame=2
        image_1 = pygame.Surface((self.width-2*frame, self.height-2*frame))
        image_1.fill((200,200,200))
        rect_1 = image_1.get_rect()
        rect_1.topleft = (self.rect.topleft[0]+frame,self.rect.topleft[1]+frame)
        image_2 = pygame.Surface((self.width-4*frame, self.height-4*frame))
        image_2.fill(self.color)
        rect_2 = image_2.get_rect()
        rect_2.topleft =(self.rect.topleft[0]+2*frame,self.rect.topleft[1]+2*frame)
        self.screen.blit(self.image, self.rect)
        self.screen.blit(image_1, rect_1)
        self.screen.blit(image_2, rect_2)
        
    def draw(self):
        self.sub_draw()
        if self.leftbutton.menu_open and not self.rightbutton.menu_open :
            self.rightbutton.draw()
            self.leftbutton.draw()
        elif not self.leftbutton.menu_open and self.rightbutton.menu_open :
            self.leftbutton.draw()
            self.rightbutton.draw()
        else :
            self.leftbutton.draw()
            self.rightbutton.draw()      

    def click(self,pos):
        if mouse_at_position(pos,self.leftbutton.position()):
            self.leftbutton.click()
        elif mouse_at_position(pos,self.rightbutton.position()):
            self.rightbutton.click()

def start_game():
    data_update()
    DISPLAYSURF = pygame.display.set_mode(
        __WINDOW_SIZE__        
    )
    pygame.display.set_caption('Minesweaper')
    board = []
    for i in range(__AMOUNT_OF_FIELDS__[0]):
        row = []
        for i in range(__AMOUNT_OF_FIELDS__[1]):
            row.append(Button())
        board.append(row)
    random_bombs(board)
    return DISPLAYSURF,board

def run_game():
    pygame.init()
    pygame.mixer.quit()
    fpsClock = pygame.time.Clock()
    DISPLAYSURF,board=start_game()
    Case_of_lose=False
    toolbar = Toolbar(__WINDOW_SIZE__[0], __TOOLBAR_SIZE__[1],DISPLAYSURF)
    t=[0,0]
    the=THE()
    while True:     
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                t[0]=pygame.mouse.get_pos()
                pos_b = position_to_button(t[0])     
            if event.type == pygame.MOUSEBUTTONUP:
                t[1]=pygame.mouse.get_pos()
                pos_a = position_to_button(t[1])
                if the.choosing :
                    the.last_will(t)
                elif toolbar.leftbutton.menu_open and toolbar.leftbutton.menu.in_range(t):
                    toolbar.leftbutton.menu.action(t)
                elif toolbar.rightbutton.menu_open and toolbar.rightbutton.menu.in_range(t):
                    toolbar.rightbutton.menu.action(t)
                elif t[1][1]<__TOOLBAR_SIZE__[1]:
                    toolbar.click(t)
                elif pos_a==pos_b:
                    the.if_end=Button_click(pos_a,board,event.button)
        draw(DISPLAYSURF,board)
        toolbar.draw()       
        the.check_end(DISPLAYSURF,board,toolbar)    
        pygame.display.update()
        fpsClock.tick(__FPS__)

if __name__ == '__main__':
    print("Hello!\nThis is my Minesweaper coded in Python 3.6")
    print("~ Patryk Walczak 7 Feb 2019")
    run_game()
