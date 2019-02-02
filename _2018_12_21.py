# 16_many_snakes.py
import random
#from collections import deque

import pygame, sys
from pygame.locals import *

#GAME_CELL_SIZE_PX = 20  # HAVE TO BE EVEN NUMBER
#assert (int(GAME_CELL_SIZE_PX/2)*2) == GAME_CELL_SIZE_PX

#GAME_CELLS_X = 40
#GAME_CELLS_Y = 30

FPS = 30  # Frames Per second
#MPS = 10 # Moves per second

#FRAMES_PER_MOVE = FPS // MPS

#random.seed(a=1)

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
#należy zabespieczyć
def random_bombs(board): 
    XSize=len(board[0])
    YSize=len(board) 
    buttons=XSize*YSize
    n=int(random.randrange(10,25)*(buttons/100))
    for i in range(0,n):
        y=random.randrange(0,YSize)
        x=random.randrange(0,XSize)
        if board[y][x].bomb == False:
            board[y][x].bomb = True
        else:
            i=i-1

def draw_segment(surface, color, x, y):
    """
    :param surface: surface to draw on
    :param x: x coord in game cells
    :param y: y coord in game cells
    :return: 
    """
    # WHITE = (255, 255, 255)
    position = (
            x * GAME_CELL_SIZE_PX,
            y * GAME_CELL_SIZE_PX,
            GAME_CELL_SIZE_PX,
            GAME_CELL_SIZE_PX
    )
    pygame.draw.rect(surface, color, position)


def draw_food(surface, x, y):
    """
    :param surface: surface to draw on
    :param x: x coord in game cells
    :param y: y coord in game cells
    :return: 
    """
    RED = (255, 0, 0)
    position = (
        x * GAME_CELL_SIZE_PX + GAME_CELL_SIZE_PX//2,
        y * GAME_CELL_SIZE_PX + GAME_CELL_SIZE_PX//2)
    pygame.draw.circle(surface, RED, position, GAME_CELL_SIZE_PX//2)


class Snake:
    vectors = {
        'UP': (0, -1),
        'DOWN': (0, 1),
        'LEFT': (-1, 0),
        'RIGHT': (1, 0),
    }
    opposites =  {
        'UP': 'DOWN',
        'DOWN': 'UP',
        'LEFT': 'RIGHT',
        'RIGHT': 'LEFT',
    }

    def __init__(
        self,
        food,
        color=(255, 255, 255),
        key_mapping=None,
        initial_segments=None,
    ):
        if initial_segments is None:
            initial_segments = deque([[0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5]])
        self.segments = initial_segments
        self.direction = 'RIGHT'
        self.last_direction = self.direction
        self.food = food
        # w kolejności wskazówek zegara ↑→↓←
        if key_mapping is None:
            key_mapping = {
                K_UP: 'UP',
                K_RIGHT: 'RIGHT',
                K_DOWN: 'DOWN',
                K_LEFT: 'LEFT',
            }
        self.keys_to_directions = key_mapping
        self.color = color

    def _is_opposite(self, test_direction, direction):
        opposite = self.opposites[direction]
        if test_direction == opposite:
            return True
        return False

    def _normalize_segments(self):
        for segment in self.segments:
            if segment[0] >= GAME_CELLS_X:
                segment[0] -= GAME_CELLS_X
            if segment[0] < 0:
                segment[0] += GAME_CELLS_X
            if segment[1] >= GAME_CELLS_Y:
                segment[1] -= GAME_CELLS_Y
            if segment[1] < 0:
                segment[1] += GAME_CELLS_Y

    def move(self):
        vector = self.vectors.get(self.direction, (0, 0))
        self.last_direction = self.direction
        # wypadałoby zalogować, że brakuje jakiegos klucza...
        first_segment = self.segments[-1]
        self.segments.append(
            # TODO: a może da się sprytniej? Coś z zip?
            [first_segment[0] + vector[0], first_segment[1] + vector[1]]
        )
        self._normalize_segments()
        if not self.try_to_eat():
            self.segments.popleft()

    def draw(self, surface):
        for segment in self.segments:
            draw_segment(surface, self.color, *segment)

    def process_event_2(self, event):
        # te stałe stringi wypadałoby do jakiś constów przenieść
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                if not self.last_direction == 'RIGHT':
                    self.direction = 'LEFT'
            elif event.key == K_RIGHT:
                if not self.last_direction == 'LEFT':
                    self.direction = 'RIGHT'
            elif event.key == K_UP:
                if not self.last_direction == 'DOWN':
                    self.direction = 'UP'
            elif event.key == K_DOWN:
                if not self.last_direction == 'UP':
                    self.direction = 'DOWN'

    def process_event(self, event):
        if event.type == KEYDOWN:
            desired_direction = self.keys_to_directions.get(event.key)
            if desired_direction:
                if not self._is_opposite(desired_direction, self.last_direction):
                    self.direction = desired_direction

    def try_to_eat(self):
        if (
            self.segments[-1][0] == self.food.x
            and self.segments[-1][1] == self.food.y
        ):
            self.food.eaten()
            return True
        return False


class FoodProvider:
    def __init__(self):
        # A tu jest subtelny bug - możemy postawić jedzenie na wężu!!!!!
        self._get_new_coords()

    def _get_new_coords(self):
        self.x = random.randrange(GAME_CELLS_X)
        self.y = random.randrange(GAME_CELLS_Y)

    def draw(self, surface):
        draw_food(surface, self.x, self.y)

    def eaten(self):
        self._get_new_coords()


def draw(surface, board):
    GROUND_COLOR = (0, 0, 50)
    BUTTON_COV = (200,200,200)
    BUTTON_UNCOV = (150,50,0)
    BUTTON_FLAG = (0,50,150)
    ground = (
        0, 0,
        640, 360
    )
    pygame.draw.rect(surface, GROUND_COLOR, ground)
    XSize=len(board[0])
    YSize=len(board)  
    border=10
    size=((ground[2]-5)/YSize,(ground[3]-5)/XSize)
    for j in range(0,XSize):
        for i in range(0,YSize):                     
            position = (
                2+border/2+size[0]*i, 2+border/2+size[1]*j,
                size[0]-border/2, size[1]-border/2
            )
            BUTTON_COLOR=BUTTON_COV
            if board[i][j].flag==False :
                BUTTON_COLOR=BUTTON_COLOR
            else:
                BUTTON_COLOR=BUTTON_FLAG

            if board[i][j].uncovered==False :
                BUTTON_COLOR=BUTTON_COLOR
            else:
                BUTTON_COLOR=BUTTON_UNCOV

            pygame.draw.rect(surface, BUTTON_COLOR, position)
            





def run_game():
    pygame.init()
    # workaround for: https://github.com/pygame/pygame/issues/331
    pygame.mixer.quit()
    fpsClock = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode(
        (640,360)#(GAME_CELLS_X * GAME_CELL_SIZE_PX, GAME_CELLS_Y * GAME_CELL_SIZE_PX)        
    )
    pygame.display.set_caption('Minesweaper')
    board= [9*[Sqr]]*16
    random_bombs(board)
    #food = FoodProvider()
    #snakes = []
    #snakes.append(Snake(food=food))
    #snakes.append(
    #    Snake(
    #        food=food,
    #        color=(0, 255, 0),
    #        key_mapping={
    #            K_w: 'UP',
    #           K_d: 'RIGHT',
    #            K_s: 'DOWN',
    #            K_a: 'LEFT',
    #        },
    #        initial_segments=deque([[0, 3], [1, 3], [2, 3], [3, 3], [4, 3], [5, 3]]),
    #    )
    #)
    #snakes.append(
    #    Snake(
    #        food=food,
    #       color=(0, 0, 255),
    #       key_mapping={
    #           K_i: 'UP',
    #           K_l: 'RIGHT',
    #            K_k: 'DOWN',
    #            K_j: 'LEFT',
    #       },
    #        initial_segments=deque([[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]]),
    #    )
    #)
    #frames_elapsed_since_last_move = 0
    while True:
        for event in pygame.event.get():
            print('event: {}'.format(event))
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    #        for snake in snakes:
    #            snake.process_event(event)
        draw(DISPLAYSURF,board)
    #    for snake in snakes:
    #        snake.draw(DISPLAYSURF)
    #    food.draw(DISPLAYSURF)
    #    frames_elapsed_since_last_move += 1
    #    if frames_elapsed_since_last_move >= FRAMES_PER_MOVE:
    #        frames_elapsed_since_last_move = 0
    #        for snake in snakes:
    #            snake.move()
        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == '__main__':
    run_game()