"""
game.py
~~~~~~~~~~

Il modulo definisce una partita di snake, che puo' essere visualizzata o meno, giocabile o meno
Viene utilizzato Pygame
"""

from map import *
from pygame.locals import *
from snake import *


class Game:
    """ Game Class """

    def __init__(self):
        self.game_score = 0     # contiene il fitness del serpente a fine partita
        self.game_time = 0      # tempo passato da quando e' iniziata la partita (utile per fermare partite con lo snake che e' andato in loop)

    def start(self, display=False, neural_net=None, playable=False, speed=20):
        """
        Funzione principale del gioco
        
        :param display: boolean mostrare o meno la partita
        :param neural_net: NeuralNetwork da passare in input perche' giochi la partita
        :param playable: boolean per giocare manualmente la partita
        :param speed: int velocita' della partita
        :return: int score
        """
        if not display:
            return self.run_invisible(neural_net=neural_net)
        else:
            return self.run_visible(neural_net=neural_net, playable=playable, speed=speed)

    
    def endGame(self):
        # time.sleep(5)
        pygame.quit()


    def run_invisible(self, neural_net=None):
        """
        Esegue una partita non visibile giocata dalla neural net

        :param neural_net: NeuralNetwork che giochera' la partita
        :return: int score
        """
        snake = Snake(neural_net=neural_net)        # creazione snake
        map = Map(snake)                            # creazione mappa

        cont = True                                 # loop del gioco
        while cont:
            self.game_time += 1
            map.scan()                              # da' visione alla neural net della mappa in un determinato istante
            snake.AI()                              # decisione della neural net in un determinato istante
            snake.update()                          # il serpente si muove e diventa piu' grande (se ha preso del cibo)
            map.update()                            # controlla collisioni con la parete o col cibo
            if not snake.alive:
                cont = False
                self.game_time = 0
        self.game_score = snake.fitness()           # se la partita finisce, ritorna lo score
        return self.game_score

    def run_visible(self, playable=False, neural_net=None, speed=20):
        """
        Esegue una partita non visibile giocata dalla neural net o manualmente

        :param playable: boolean per giocare manualmente o meno
        :param neural_net: NeuralNetwork che giochera' alla partita
        :param speed: int velocita' della partita
        :return: int score
        """
        pygame.init()                                                               # inizializzazione pygame
        game_window = pygame.display.set_mode((int(WINDOW_SIZE*2), WINDOW_SIZE))    # apre la finestra
        pygame.display.set_caption(WINDOW_TITLE)

        snake = Snake(neural_net=neural_net)
        map = Map(snake)

        cont = [True]
        while cont[0]:                               # loop del gioco
            pygame.time.Clock().tick(speed)          # mostra la velocita'
            self.inputs_management(snake, cont)      # gestione degli input
            if not playable:
                map.scan()                           # da' visione alla neural net della mappa in un determinato istante
                snake.AI()                           # decisione della neural net in un determinato istante
            self.render(game_window, map)            # rendering del frame
            snake.update()
            map.update()
            if not snake.alive:
                cont[0] = False

        self.game_score = snake.fitness()            # se la partita finisce, ritorna lo score
        return self.game_score

    def inputs_management(self, snake, cont):
        """ Gestione degli input da tastiera """
        
        for event in pygame.event.get():
            if event.type == QUIT:
                cont[0] = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:       # escape
                    cont[0] = False
                if event.key == K_RIGHT:        # right
                    snake.turn_right()
                elif event.key == K_LEFT:       # left
                    snake.turn_left()
                elif event.key == K_UP:         # up
                    pass

    def render(self, window, map):
        """ Renderizza la partita """
        
        map.render(window)
        pygame.display.flip()
