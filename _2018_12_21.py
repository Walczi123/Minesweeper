from random import randrange
import pygame, sys
from pygame.locals import *
from math import ceil,floor,frexp

# # # TO CHANGE # # #
__FPS__ = 60  # Frames Per second
__AMOUNT_OF_BOMBS__=(16,9) # Numbers of bombs at row, at column
__BUTTON_SIZE__=(40,40) #Size of button without perimeter

# # # NOT TO CHANGE # # #
__BORDER__=((0.25*__BUTTON_SIZE__[0])/2,(0.25*__BUTTON_SIZE__[1])/2)  #Perimeter of button
__PERIMETER__=((0.1*__BUTTON_SIZE__[0])//2,(0.1*__BUTTON_SIZE__[1])//2) #Perimeter of window
__WINDOW_SIZE__=(int(__AMOUNT_OF_BOMBS__[0]*__BUTTON_SIZE__[0]+__PERIMETER__[0]*4),int(__AMOUNT_OF_BOMBS__[1]*__BUTTON_SIZE__[1]+__PERIMETER__[1]*4)) #Size of widows


def mantissa(x):
    return x-floor(x)

class Sqr:
    """
    bool bomb - True if in object Sqr is a bomb, False otherwise
    bool flag - True if in object Sqr is a flag, False otherwise
    bool uncovered - False if object is covered, True otherwise
    """
    bomb=False
    flag=False
    uncovered=False

    def __init__(
        self, 
        bomb=False, 
        flag=False, 
        uncovered=False,
                 ): 
        if type(bomb)is not bool : bomb = False 
        if type(flag)is not bool : flag = False
        if type(flag)is not bool : uncovered = False
        self.bomb=bomb   
        self.flag=flag
        self.uncovered=uncovered

def random_bombs(board=None):  
    if board==None: return
    buttons=__AMOUNT_OF_BOMBS__[0]*__AMOUNT_OF_BOMBS__[1]
    n=int(randrange(10,25)*(buttons/100))
    for i in range(0,n):
        y=randrange(0,__AMOUNT_OF_BOMBS__[0])
        x=randrange(0,__AMOUNT_OF_BOMBS__[1])
        if board[y][x].bomb == False:
            board[y][x].bomb = True
        else:
            i=i-1

def draw(surface, board):
    GROUND_COLOR = (0, 0, 50)
    BUTTON_COV = (200,200,200)
    BUTTON_UNCOV = (150,50,0)
    BUTTON_FLAG = (0,50,150)
    ground = (
        0, 0,
        __WINDOW_SIZE__[0],__WINDOW_SIZE__[1]
    )
    pygame.draw.rect(surface, GROUND_COLOR, ground)    
    for j in range(0,__AMOUNT_OF_BOMBS__[1]):
        for i in range(0,__AMOUNT_OF_BOMBS__[0]):                     
            position = (
                __PERIMETER__[0]+__BORDER__[0]+__BUTTON_SIZE__[0]*i,__PERIMETER__[1]+__BORDER__[1]+__BUTTON_SIZE__[1]*j, 
                __BUTTON_SIZE__[0]-__BORDER__[0],__BUTTON_SIZE__[1]-__BORDER__[1]
            )
            BUTTON_COLOR=BUTTON_COV
            if board[i][j].flag==True :
                BUTTON_COLOR=BUTTON_FLAG
            if board[i][j].uncovered==True:
                BUTTON_COLOR=BUTTON_UNCOV
            pygame.draw.rect(surface, BUTTON_COLOR, position)
    
def position_to_button(pos):
    button_pos=((pos[0]-__PERIMETER__[0])/__BUTTON_SIZE__[0],(pos[1]-__PERIMETER__[1])/__BUTTON_SIZE__[1])
    t=False
    #if |floor(button(x))-center_of_buttron(x))| <= (center_of_buttron(x)-border(x)) and |floor(button(y))-center_of_buttron(y))| <= (center_of_buttron(y)-border(y)):
    if abs((int(mantissa(button_pos[0])*__BUTTON_SIZE__[0])%__BUTTON_SIZE__[0])-__BUTTON_SIZE__[0]/2) <= ((__BUTTON_SIZE__[0]/2)-__BORDER__[0]):
        if abs((int(mantissa(button_pos[1])*__BUTTON_SIZE__[1])%__BUTTON_SIZE__[1])-__BUTTON_SIZE__[1]/2) <= ((__BUTTON_SIZE__[1]/2)-__BORDER__[1]):
            t=True
    button_pos=(ceil(button_pos[0]),ceil(button_pos[1]))
    return (t,button_pos[0]-1,button_pos[1]-1)
            
def MouseClick(input, board):
    t,y,x = input
    if t and board[y][x].uncovered==False:
        print("uncover button ",y,x)
        board[y][x].uncovered=True

def run_game():
    pygame.init()
    pygame.mixer.quit()
    fpsClock = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode(
        __WINDOW_SIZE__        
    )
    pygame.display.set_caption('Minesweaper')
    board = []
    for i in range(__AMOUNT_OF_BOMBS__[0]):
        row = []
        for i in range(__AMOUNT_OF_BOMBS__[1]):
            row.append(Sqr())
        board.append(row)
    pos_a=0
    while True:
        for event in pygame.event.get():
            print('event: {}'.format(event))
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_b = position_to_button(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONUP:
                pos_a = position_to_button(pygame.mouse.get_pos())
                if pos_a==pos_b:
                    MouseClick(pos_a,board)

        draw(DISPLAYSURF,board)
        pygame.display.update()
        fpsClock.tick(__FPS__)

if __name__ == '__main__':
    run_game()