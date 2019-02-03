from random import randrange
import pygame, sys
from pygame.locals import *
from math import ceil, floor

# # # TO CHANGE # # #
__FPS__ = 30  # Frames Per second
__AMOUNT_OF_FIELDS__=(12,6) # Numbers of bombs at row, at column
__BUTTON_SIZE__=(40,40) #Size of button without perimeter

# # # NOT TO CHANGE # # #
__BORDER__=((0.25*__BUTTON_SIZE__[0])/2,(0.25*__BUTTON_SIZE__[1])/2)  #Perimeter of button
__PERIMETER__=((0.1*__BUTTON_SIZE__[0])//2,(0.1*__BUTTON_SIZE__[1])//2) #Perimeter of window
__WINDOW_SIZE__=(int(__AMOUNT_OF_FIELDS__[0]*__BUTTON_SIZE__[0]+__PERIMETER__[0]*4),int(__AMOUNT_OF_FIELDS__[1]*__BUTTON_SIZE__[1]+__PERIMETER__[1]*4)) #Size of widows
__PERCENTAGE_OF_BOMBS__=(8,10) # (x,y) x-lower bound of percentage of all fields of bombs, y - upper bound
__FONT_SIZE__=int(0.75*__BUTTON_SIZE__[1]) #Size of number in field
__FONT__='freesansbold.ttf' #Font of number in field
__AMOUNT_OF_BOMBS__=0 #Amount of bombs, changed after addition of bombs
__AMOUNT_OF_NON_BOMBS__=(__AMOUNT_OF_FIELDS__[0])*(__AMOUNT_OF_FIELDS__[1]) #Amount of fields without bombs
__UNCOVERED_FIELDS__=0 #Number of uncovered fields
__END__=False #If user uncover field with bomb then True, and game has ended

def mantissa(x):
    return x-floor(x)

class Sqr:
    """
    bool bomb - True if in object Sqr is a bomb, False otherwise
    int number - Amount of bombs in adjacent fields ,default = 0
    bool flag - True if in object Sqr is a flag, False otherwise
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
                __PERIMETER__[0]+__BORDER__[0]+__BUTTON_SIZE__[0]*i,__PERIMETER__[1]+__BORDER__[1]+__BUTTON_SIZE__[1]*j, 
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
    button_pos=((pos[0]-__PERIMETER__[0])/__BUTTON_SIZE__[0],(pos[1]-__PERIMETER__[1])/__BUTTON_SIZE__[1])
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
    global __UNCOVERED_FIELDS__,__AMOUNT_OF_FIELDS__
    if board[y][x].uncovered == False :
        board[y][x].uncovered = True
        __UNCOVERED_FIELDS__=__UNCOVERED_FIELDS__+1    
    if board[y][x].number == 0 :
        for i in range(0,3):
            for j in range(0,3):
               if x-1+i>=0 and y-1+j>=0 and x-1+i<__AMOUNT_OF_FIELDS__[1] and y-1+j<__AMOUNT_OF_FIELDS__[0]:
                   if (i,j)!=(1,1) :                   
                        Uncover_field(board,y-1+j,x-1+i)

def err(board):
    a=0
    for i in range(0,__AMOUNT_OF_FIELDS__[0]) :
         for j in range(0,__AMOUNT_OF_FIELDS__[1]):
             if board[i][j].uncovered : a+=1
    return a

def Lose_end(surface):
    pygame.display.update()
    pygame.time.wait(1000)
    rec=(__WINDOW_SIZE__[0]/2 -115, __WINDOW_SIZE__[1]/2 - 55, 230, 110)
    pygame.draw.rect(surface, (255,0,0), rec)
    rec=(__WINDOW_SIZE__[0]/2 -110, __WINDOW_SIZE__[1]/2 - 50, 220, 100)
    pygame.draw.rect(surface, (255,255,255), rec)
    message_display("You Fail !!!",__WINDOW_SIZE__[1]/2 -10,__WINDOW_SIZE__[0]/2,surface,(0,0,0),__FONT__,30)   
    message_display("Try Again",__WINDOW_SIZE__[1]/2 + 20,__WINDOW_SIZE__[0]/2,surface,(0,0,0),__FONT__,20)   
    pygame.display.update()
    pygame.time.wait(2500)
    pygame.quit()
    sys.exit()

def Win_end(surface):
    pygame.display.update()
    pygame.time.wait(1000)
    rec=(__WINDOW_SIZE__[0]/2 -115, __WINDOW_SIZE__[1]/2 - 55, 230, 110)
    pygame.draw.rect(surface, (0,150,0), rec)
    rec=(__WINDOW_SIZE__[0]/2 -110, __WINDOW_SIZE__[1]/2 - 50, 220, 100)
    pygame.draw.rect(surface, (255,255,255), rec)
    message_display("You Win !!!",__WINDOW_SIZE__[1]/2 -10,__WINDOW_SIZE__[0]/2,surface,(0,0,0),__FONT__,30)   
    message_display("Try Again",__WINDOW_SIZE__[1]/2 + 20,__WINDOW_SIZE__[0]/2,surface,(0,0,0),__FONT__,20)   
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

def MouseClick(input=None, board=None, button=None):
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

def Case_of_win():
    global __UNCOVERED_FIELDS__,__AMOUNT_OF_NON_BOMBS__
    if __UNCOVERED_FIELDS__==__AMOUNT_OF_NON_BOMBS__ : #__AMOUNT_OF_FIELDS__[0]*__AMOUNT_OF_FIELDS__[1]-__AMOUNT_OF_BOMBS__:      
        return True
    return False

def run_game():
    pygame.init()
    pygame.mixer.quit()
    fpsClock = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode(
        __WINDOW_SIZE__        
    )
    pygame.display.set_caption('Minesweaper')
    board = []
    for i in range(__AMOUNT_OF_FIELDS__[0]):
        row = []
        for i in range(__AMOUNT_OF_FIELDS__[1]):
            row.append(Sqr())
        board.append(row)
    random_bombs(board)
    pos_a=0
    end=False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_b = position_to_button(pygame.mouse.get_pos())               
            if event.type == pygame.MOUSEBUTTONUP:
                pos_a = position_to_button(pygame.mouse.get_pos())
                if pos_a==pos_b:
                    end=MouseClick(pos_a,board,event.button)
                print("Odkryte pola",err(board),__UNCOVERED_FIELDS__ )
                print("ilosc pol zakrytych",__AMOUNT_OF_FIELDS__[0]*__AMOUNT_OF_FIELDS__[1] - __UNCOVERED_FIELDS__)
        draw(DISPLAYSURF,board)
        pygame.display.update()
        if end : 
            Uncoverall(board)
            draw(DISPLAYSURF,board)
            Lose_end(DISPLAYSURF)
        if Case_of_win() :
            Uncoverall(board)
            draw(DISPLAYSURF,board)
            Win_end(DISPLAYSURF)
       
        fpsClock.tick(__FPS__)

if __name__ == '__main__':
    run_game()