"""
neural_network.py
~~~~~~~~~~

Questo modulo è utilizzato per la costruzione di DNN

Pesi e bias sono inizializzati casualmente secondo una distribuzione di Gauss
Una neural net puo' essere salvata e caricata a piacimento

Non viene implementata la back-propagation dato che utilizzeremo l'algoritmo genetico
"""

from numba import jit
import numpy as np
import pygame
from constants import *
from pygame import gfxdraw


class NeuralNetwork:
    """ Neural Network class """

    def __init__(self, shape=None):
        """
        Funzione d'inizializzazione
        
        :param shape: lista di int, descrive i layer e i neuroni per layer della neural net
        """
        self.shape = shape
        self.biases = []
        self.weights = []
        self.score = 0        # punteggio per sapere quanto ha giocato bene
        if shape:
            for y in shape[1:]:                             # inizializzazione casuale dei bias
                self.biases.append(np.random.randn(y, 1))
            for x, y in zip(shape[:-1], shape[1:]):         # inizializzazione casuale dei pesi
                self.weights.append(np.random.randn(y, x))

    def feed_forward(self, a):
        """
        Funzione principale, prende un vettore input e ne calcola l'output tramite forward-propagation

        :param a: colonna di integer, input per la neural net (visione del serpente)
        :return: colonna di integer, attivazione dei neuroni output
        """
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b)
        return a

    def save(self, name=None):
        """
        Salva i pesi e bias in due file separati nella cartella attuale

        :param name: stringa, in caso volessi darle un nome
        :return: crea due file
        """
        if not name:
            np.save('saved_weights_'+str(self.score), self.weights)
            np.save('saved_biases_'+str(self.score), self.biases)
        else:
            np.save(name + '_weights', self.weights)
            np.save(name + '_biases', self.biases)

    def load(self, filename_weights, filename_biases):
        """
        Carica pesi e bias di neural net salvate da 2 file all'interno dell'oggetto neural net

        :param filename_weights: file contenente i pesi salvati
        :param filename_biases: file contenente i bias salvati
        """
        self.weights = np.load(filename_weights, allow_pickle=True)
        self.biases = np.load(filename_biases, allow_pickle=True)

    def render(self, window, vision):
        """
        Mostra la neural net allo stato corrente nella parte destra della finestra di gioco

        La funzione supporta qualsiasi forma di neural net fintantoche' i neuroni di input e output siano quelli giusti (21 di input, 3 di output)
        I plan to work on it for later projects

        :param window: finestra di gioco
        :param vision: lista di int, "vista" del serpente necessaria a mostrare gli input
        """
        network = [np.array(vision)]            # conterra' tutte le attivazioni dei neuroni per ogni layer
        for i in range(len(self.biases)):
            activation = sigmoid(np.dot(self.weights[i], network[i]) + self.biases[i])  # elabora l'attivazione dei neuroni
            network.append(activation)                                                  # la mette in append

        screen_division = WINDOW_SIZE / (len(network) * 2)     # elabora la distanza fra i layer relativamente alle dimensioni della finestra
        step = 1
        for i in range(len(network)):                                           # per ogni layer
            for j in range(len(network[i])):                                    # e per ogni neurone nel layer attuale
                y = int(WINDOW_SIZE/2 + (j*24) - (len(network[i])-1)/2 * 24)    # posizione del neurone
                x = int(WINDOW_SIZE + screen_division * step)
                intensity = int(network[i][j][0] * 255)                         # intensita' del neurone

                if i < len(network)-1:
                    for k in range(len(network[i+1])):                                          # archi
                        y2 = int(WINDOW_SIZE/2 + (k * 24) - (len(network[i+1]) - 1) / 2 * 24)   # posizione target degli archi
                        x2 = int(WINDOW_SIZE + screen_division * (step+2))
                        pygame.gfxdraw.line(window, x, y, x2, y2,                               # renderizza la connessione
                                            (intensity/2+30, intensity/2+30, intensity/2+30, intensity/2+30))

                pygame.gfxdraw.filled_circle(window, x, y, 9, (intensity, intensity, intensity))    # renderizza il neurone
                pygame.gfxdraw.aacircle(window, x, y, 9, (205, 205, 205))
            step += 2

@jit(nopython=True)
def sigmoid(z):
    """
    Funzione sigmoidea, per l'attivazione dei neuroni
    @jit e' utilizzato per velocizzare l'elaborazione
    """
    return 1.0 / (1.0 + np.exp(-z))
