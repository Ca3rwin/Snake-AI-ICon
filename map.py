"""
map.py
~~~~~~~~~~

Questo modulo e' utilizzato per la creazione della mappa del gioco

La mappa:\n
- Contiene la propria morfologia in una matrice (vedi MAP in constants.py)
- Contiene un'istanza di snake ed una di food (il cibo spawna uno per volta)
- Si occupa della gestione delle collisioni, creazione di cibo e di passare ogni stato della partita alla neural net
"""

import traceback
import math
import random
import numpy as np
from snake import *


class Map:
    """Map class"""

    def __init__(self, snake):
        self.structure = MAP                                            # matrice di 0 ed 1 rappresentanti la mappa
        self.snake = snake                                              # il serpente che si muove e cresce nella mappa
        self.food = [random.randint(8, 12), random.randint(8, 12)]      # cibo, lista di 2 coordinate (viene inizializzato relativamente vicino al centro della mappa)

    def update(self):
        """
        Controlla se ci sono collisioni fra la testa del serpente ed una parete o del cibo\n
        Aggiorna lo stato della partita in caso di collisione
        """
        snake_head_x, snake_head_y = self.snake.head
        snake_pos = self.structure[snake_head_y][snake_head_x]
        # print("snake_head_x POST")
        # print(snake_head_x)
        if [snake_head_x, snake_head_y] == self.food:                   # se la testa del serpente si trova su del cibo
            self.snake.grow()                                           # il serpente cresce e viene creato nuovo cibo
            self.add_food(random.randint(0, SPRITE_NUMBER - 1),
                          random.randint(0, SPRITE_NUMBER - 1))
        elif snake_pos == WALL:                                         # se la testa del serpente è su una parete, muore
            self.snake.alive = False

    def add_food(self, block_x, block_y):
        """
        Adds food on (block_x, block_y) position
        """
        self.food = [block_x, block_y]
        try:
            if self.structure[block_x][block_y] == 0:                   # checks if food will spawn in a free space (no wall, wall bad)
                for i in self.snake.body:                               # checks if food will spawn where the snake is
                    if i == [block_x, block_y]:
                        # Cibo spawnato nel serpente, respawn...
                        self.add_food(random.randint(0, SPRITE_NUMBER - 1), random.randint(0, SPRITE_NUMBER - 1))
            else:
                # Cibo spawnato nella parete, respawn
                self.add_food(random.randint(0, SPRITE_NUMBER - 1), random.randint(0, SPRITE_NUMBER - 1))
            
        except Exception: 
            traceback.print_exc()
            pygame.quit()

    def render(self, window):
        """
        Renders the map (background, walls and food) on the game window and calls render() of snake
        Very very very unoptimized since render does not affect the genetic algorithm

        :param window: surface window
        """
        wall = pygame.image.load(IMAGE_WALL).convert()          # loading images
        food = pygame.image.load(IMAGE_FOOD).convert_alpha()

        window.fill([0,0,0])                # painting background
        num_line = 0
        for line in self.structure:         # running through the map structure
            num_case = 0
            for sprite in line:
                x = num_case * SPRITE_SIZE
                y = num_line * SPRITE_SIZE
                if sprite == 1:                         # displaying wall
                    window.blit(wall, (x, y))
                if self.food == [num_case, num_line]:   # displaying food
                    window.blit(food, (x, y))
                num_case += 1
            num_line += 1
        self.snake.render(window)         # snake will be rendered on above the map



    def scan(self):
        """
        Scans the snake's environment into the 'scan' variable (list of lists) and gives it to snake's vision

        Notes:
        - 7 first inputs are for walls, 7 next for food, 7 last for itself (its body)
        - Food is seen across all the map, walls and body are seen in range of 10 blocks max
        - This method is long and I do not factorise much for performance issues,
          the structure is easily understandable anyway

        :return: nothing but gives vision to the snake
        """
        def scan_wall(direction_x, direction_y, direction_range):
            """
            Looks for a wall in the direction given in parameters for 10 steps max

            I decided to use inner methods for a compromise between performance and factorisation

            :param direction_x: direction in x axis, can be 1, 0 or -1 for "right", "stay" and "left" respectively
            :param direction_y: direction in y axis, can be 1, 0 or -1 for "down", "stay" and "up" respectively
            :param direction_range: maximum range to scan
            :return: number with 0 value if nothing or 1/distance to wall if wall's detected
            """
            res = 0
            for i in range(1, 10):                      # looking up to 10 blocks max
                step_x = head_x + i * direction_x       # coordinates of next block to check
                step_y = head_y + i * direction_y

                if i < direction_range:
                    if structure[step_y][step_x] == WALL:                       # if wall is detected in current block
                        res = 1 / distance((head_x, head_y), (step_x, step_y))  # returns 1/distance to the block
            return res

        def scan_self(direction_x, direction_y, direction_range):
            """
            Looks for a snake's body block in the direction given in parameters for 10 steps max

            :params see "scan_wall", same params
            :return: number with 0 value if nothing or 1/distance to body if a body block is detected
            """
            res = 0
            for i in range(1, 10):
                step_x = head_x + i * direction_x
                step_y = head_y + i * direction_y

                if i < direction_range:
                    if [step_x, step_y] in snake_body:
                        res = max(res, 1 / distance((head_x, head_y), (step_x, step_y)))
            return res

        def scan_food(direction_x, direction_y, direction_range):
            """
            Looks for food in the direction given in parameters until range is reached

            :params see "scan_wall", same params
            :return: number with 0 value if nothing or 1/distance to body if a body block is detected
            """
            res = 0
            for i in range(1, direction_range):
                if food_x == (head_x + i * direction_x) and food_y == (head_y + i * direction_y):
                    res = 1
            return res

        scan = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]    # default value
        structure = self.structure
        snake_body = self.snake.body                # making local variables for readability and performance
        head_x = self.snake.head[0]
        head_y = self.snake.head[1]
        food_x = self.food[0]
        food_y = self.food[1]

        forward_x = self.snake.direction[0]         # calculating each coordinate for each 7 directions
        forward_y = self.snake.direction[1]         # since the snake sees in FIRST PERSON
        right_x = -forward_y
        right_y = forward_x
        left_x = forward_y                          # for example, if snake's looking in [1,0] direction (down)
        left_y = -forward_x                         # its left is [1,0] (right for us because we look from above)
        forward_right_x = forward_x + right_x
        forward_right_y = forward_y + right_y
        forward_left_x = forward_x + left_x
        forward_left_y = forward_y + left_y         # see snake.py class for better explanations
        backward_right_x = -forward_left_x
        backward_right_y = -forward_left_y
        backward_left_x = -forward_right_x
        backward_left_y = -forward_right_y

        forward_range = (20 - (forward_x * head_x + forward_y * head_y) - 1) % 19 + 1   # computing max range
        backward_range = 21 - forward_range                                             # for each direction
        right_range = (20 - (right_x * head_x + right_y * head_y) - 1) % 19 + 1
        left_range = 21 - right_range
        forward_right_range = min(forward_range, right_range)           # values are hard encoded
        forward_left_range = min(forward_range, left_range)             # since I'm not planning on making it modifiable
        backward_right_range = min(backward_range, right_range)
        backward_left_range = min(backward_range, left_range)

        scan[0][0] = scan_wall(forward_x, forward_y, forward_range)                 # scanning walls in all directions
        scan[1][0] = scan_wall(right_x, right_y, right_range)
        scan[2][0] = scan_wall(left_x, left_y, left_range)
        scan[3][0] = scan_wall(forward_right_x, forward_right_y, forward_right_range)
        scan[4][0] = scan_wall(forward_left_x, forward_left_y, forward_left_range)
        scan[5][0] = scan_wall(backward_right_x, backward_right_y, backward_right_range)
        scan[6][0] = scan_wall(backward_left_x, backward_left_y, backward_left_range)

        scan[7][0] = scan_food(forward_x, forward_y, forward_range)                 # scanning food in all directions
        scan[8][0] = scan_food(right_x, right_y, right_range)
        scan[9][0] = scan_food(left_x, left_y, left_range)
        scan[10][0] = scan_food(forward_right_x, forward_right_y, forward_right_range)
        scan[11][0] = scan_food(forward_left_x, forward_left_y, forward_left_range)
        scan[12][0] = scan_food(backward_right_x, backward_right_y, backward_right_range)
        scan[13][0] = scan_food(backward_left_x, backward_left_y, backward_left_range)

        scan[14][0] = scan_self(forward_x, forward_y, forward_range)                # scanning body in all directions
        scan[15][0] = scan_self(right_x, right_y, right_range)
        scan[16][0] = scan_self(left_x, left_y, left_range)
        scan[17][0] = scan_self(forward_right_x, forward_right_y, forward_right_range)
        scan[18][0] = scan_self(forward_left_x, forward_left_y, forward_left_range)
        scan[19][0] = scan_self(backward_right_x, backward_right_y, backward_right_range)
        scan[20][0] = scan_self(backward_left_x, backward_left_y, backward_left_range)

        self.snake.vision = scan    # gives snake vision


@jit(nopython=True)
def distance(p1=None, p2=None):
    """
    Gives euclidian distance between two points
    @jit is used to speed up computation

    :param p1: origin point
    :param p2: end point
    :return: distance
    """
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


