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
        """ Genera cibo nella posizione (block_x, block_y) """
        
        self.food = [block_x, block_y]
        try:
            if self.structure[block_x][block_y] == 0:                   # controlla che il cibo si generi in una posizione libera della mappa
                for i in self.snake.body:
                    if i == [block_x, block_y]:
                        # Cibo generato nel serpente
                        self.add_food(random.randint(0, SPRITE_NUMBER - 1), random.randint(0, SPRITE_NUMBER - 1))
            else:
                # Cibo generato nella parete
                self.add_food(random.randint(0, SPRITE_NUMBER - 1), random.randint(0, SPRITE_NUMBER - 1))
            
        except Exception: 
            traceback.print_exc()
            pygame.quit()

    def render(self, window):
        """
        Renderizza la mappa (sfondo, pareti e cibo) e il serpente

        :param window: finestra del gioco
        """
        wall = pygame.image.load(IMAGE_WALL).convert()          # caricamento immagini
        food = pygame.image.load(IMAGE_FOOD).convert_alpha()

        window.fill([0,0,0])                # "dipinge" lo sfondo
        num_line = 0
        for line in self.structure:         # itera per ogni vettore della matrice MAP
            num_case = 0
            for sprite in line:
                x = num_case * SPRITE_SIZE
                y = num_line * SPRITE_SIZE
                if sprite == 1:                         # mostra parete
                    window.blit(wall, (x, y))
                if self.food == [num_case, num_line]:   # mostra cibo
                    window.blit(food, (x, y))
                num_case += 1
            num_line += 1
        self.snake.render(window)         # il serpente verrà renderizzato sopra la mappa



    def scan(self):
        """
        Controlla lo stato della partita e lo mette nella variabile 'scan' (lista di liste), che verra' poi passata alla neural net

        NB:\n
        - I primi 7 input sono per la parete, i successivi 7 per il cibo, gli ultimi 7 per il corpo del serpente
        - Il cibo e' visto attraverso tutta la mappa, mentre pareti e corpo del serpente sono visti solo ad una distanza di
          massimo 10 blocchi dalla testa

        :return: niente ma rende la mappa visibile alla neural net
        """
        def scan_wall(direction_x, direction_y, direction_range):
            """
            Controlla se c'e' una parete nella direzione data nei parametri entro 10 blocchi

            :param direction_x: direzione nell'asse x, puo' essere 1, 0 o -1 per "destra", "dritto" e "sinistra"
            :param direction_y: direzione nell'asse y, puo' essere 1, 0 o -1 per "giù", "dritto" o "su"
            :param direction_range: range massimo da controllare
            :return: int con valore 0 se non e' stata trovata una parete, altrimenti ha come valore 1/distanza dalla parete
            """
            res = 0
            for i in range(1, 10):                      # controlla fino a 10 blocchi di distanza
                step_x = head_x + i * direction_x       # coordinate del prossimo blocco da controllare
                step_y = head_y + i * direction_y

                if i < direction_range:
                    if structure[step_y][step_x] == WALL:                       # se viene trovata una parete nel blocco attuale
                        res = 1 / distance((head_x, head_y), (step_x, step_y))  # ritorna 1/distanza dal blocco
            return res

        def scan_iself(direction_x, direction_y, direction_range):
            """
            Controlla se c'e' il corpo del serpente nella direzione data nei parametri entro 10 blocchi

            :param direction_x: direzione nell'asse x, puo' essere 1, 0 o -1 per "destra", "dritto" e "sinistra"
            :param direction_y: direzione nell'asse y, puo' essere 1, 0 o -1 per "giù", "dritto" o "su"
            :param direction_range: range massimo da controllare
            :return: int con valore 0 se non e' stata trovata una parete, altrimenti ha come valore 1/distanza dal corpo
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
            Controlla se c'e' del cibo nella direzione data nei parametri finché entro ``direction_range`` blocchi

            :param direction_x: direzione nell'asse x, puo' essere 1, 0 o -1 per "destra", "dritto" e "sinistra"
            :param direction_y: direzione nell'asse y, puo' essere 1, 0 o -1 per "giù", "dritto" o "su"
            :param direction_range: range massimo da controllare
            :return: int con valore 0 se non e' stata trovata una parete, altrimenti ha come valore 1/distanza dal cibo
            """
            res = 0
            for i in range(1, direction_range):
                if food_x == (head_x + i * direction_x) and food_y == (head_y + i * direction_y):
                    res = 1
            return res

        scan = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]    # valore di default
        structure = self.structure
        snake_body = self.snake.body                # creazione di variabili locali per leggibilita' e performance
        head_x = self.snake.head[0]
        head_y = self.snake.head[1]
        food_x = self.food[0]
        food_y = self.food[1]

        forward_x = self.snake.direction[0]         # calcola ogni coordinata per tutte e 7 le direzioni
        forward_y = self.snake.direction[1]         # questo perché il serpente vede in "prima persona"
        right_x = -forward_y
        right_y = forward_x
        left_x = forward_y                          # per esempio, se il serpente guarda nella direzione [1,0] (giu')
        left_y = -forward_x                         # la sua sinistra è [1,0] (destra per noi che guardiamo "dall'alto")
        forward_right_x = forward_x + right_x
        forward_right_y = forward_y + right_y
        forward_left_x = forward_x + left_x
        forward_left_y = forward_y + left_y         # guarda la classe snake.py per migliori spiegazioni
        backward_right_x = -forward_left_x
        backward_right_y = -forward_left_y
        backward_left_x = -forward_right_x
        backward_left_y = -forward_right_y

        forward_range = (20 - (forward_x * head_x + forward_y * head_y) - 1) % 19 + 1   # elaborazione del range massimo
        backward_range = 21 - forward_range                                             # per ogni direzione
        right_range = (20 - (right_x * head_x + right_y * head_y) - 1) % 19 + 1
        left_range = 21 - right_range
        forward_right_range = min(forward_range, right_range)           # i valori sono memorizzati in modo grezzo
        forward_left_range = min(forward_range, left_range)
        backward_right_range = min(backward_range, right_range)
        backward_left_range = min(backward_range, left_range)

        scan[0][0] = scan_wall(forward_x, forward_y, forward_range)                 # cerca le pareti in tutte le direzioni
        scan[1][0] = scan_wall(right_x, right_y, right_range)
        scan[2][0] = scan_wall(left_x, left_y, left_range)
        scan[3][0] = scan_wall(forward_right_x, forward_right_y, forward_right_range)
        scan[4][0] = scan_wall(forward_left_x, forward_left_y, forward_left_range)
        scan[5][0] = scan_wall(backward_right_x, backward_right_y, backward_right_range)
        scan[6][0] = scan_wall(backward_left_x, backward_left_y, backward_left_range)

        scan[7][0] = scan_food(forward_x, forward_y, forward_range)                 # cerca cibo in tutte le direzioni
        scan[8][0] = scan_food(right_x, right_y, right_range)
        scan[9][0] = scan_food(left_x, left_y, left_range)
        scan[10][0] = scan_food(forward_right_x, forward_right_y, forward_right_range)
        scan[11][0] = scan_food(forward_left_x, forward_left_y, forward_left_range)
        scan[12][0] = scan_food(backward_right_x, backward_right_y, backward_right_range)
        scan[13][0] = scan_food(backward_left_x, backward_left_y, backward_left_range)

        scan[14][0] = scan_self(forward_x, forward_y, forward_range)                # cerca parti del proprio corpo in tutte le direzioni
        scan[15][0] = scan_self(right_x, right_y, right_range)
        scan[16][0] = scan_self(left_x, left_y, left_range)
        scan[17][0] = scan_self(forward_right_x, forward_right_y, forward_right_range)
        scan[18][0] = scan_self(forward_left_x, forward_left_y, forward_left_range)
        scan[19][0] = scan_self(backward_right_x, backward_right_y, backward_right_range)
        scan[20][0] = scan_self(backward_left_x, backward_left_y, backward_left_range)

        self.snake.vision = scan    # da' "visione" al serpente


@jit(nopython=True)
def distance(p1=None, p2=None):
    """
    Fornisce la distanza euclidea fra due punti\n
    @jit e' utilizzato per velocizzare l'elaborazione

    :param p1: punto d'origine
    :param p2: punto finale
    :return: distanza
    """
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


