"""
snake.py
~~~~~~~~~~

Questo modulo e' utilizzato per creare il serpente nel gioco

Il serpente:\n
- E' codificato come una lista, ogni elemento e' un blocco del corpo (contenente le sue coordinate)
- Ha una testa che punta al primo blocco, una direzione e viene passato alla rete neurale
- Ha visione della mappa (metodo ``map.scan()``)
- Gestisce il proprio movimento, invecchia e cresce mettendo un nuovo blocco alla sua coda quando mangia
- Ritorna il proprio fitness in base alla propria eta' e lunghezza
"""

from neural_network import *


class Snake:
    """Snake Class"""

    def __init__(self, neural_net=None, xMaxSize = 20, yMaxSize = 20):
        """
        Funzione di inizializzazione
        
        :param neural_net (NeuralNetwork): Neural net che dovra' gestire il movimento del serpente
        """
        self.body = [[10, 10], [9, 10], [9, 11], [9, 12]]       # il serpente e' una lista di coordinate
        self.head = self.body[0][:]                             # blocco della testa
        self.old_tail = self.head[:]                            # utile per la crescita
        self.direction = RIGHT
        self.age = 0
        self.starve = 500                                       # utile per evitare che il serpente vada in loop infinito
        self.alive = True
        self.neural_net = neural_net
        self.vision = []                                        # memorizza lo stato della mappa ad ogni momento
        self.xMaxSize = xMaxSize
        self.yMaxSize = yMaxSize

    def update(self):
        """ Gestisce l'eta' e la fame del serpente, che ad ogni iterazione diventera' piu' vecchio e affamato """
        
        self.age += 1
        self.starve -= 1
        if self.starve < 1:
            self.alive = False
        self.move()

    def grow(self):
        """
        Fa crescere il serpente di un blocco\n
        Chiamato da ``map.update()`` quando la testa del serpente collide con del cibo
        """
        self.starve = 500                   # utile per evitare che i serpenti vadano in loop infinito
        self.body.append(self.old_tail)     # mette un nuovo blocco in append alla coda

    def move(self):
        """ Fa muovere il serpente, la testa si muove nella direzione attuale ed ogni blocco sostituisce il predecessore """
        self.old_tail = self.body[-1][:]        # salva la precedente posizione dell'ultimo blocco
        self.head[0] += self.direction[0]       # muove la testa
        self.head[1] += self.direction[1]
        
        self.head[0] = (self.head[0] + self.xMaxSize) % self.xMaxSize
        self.head[1] = (self.head[1] + self.yMaxSize) % self.yMaxSize
        
        if self.head in self.body[1:]:          # se il serpente si colpisce muore
            self.alive = False
        self.body.insert(0, self.body.pop())    # ogni blocco rimpiazza il predecessore
        self.body[0] = self.head[:]             # il primo blocco e' la testa

    def turn_right(self):
        """
        Fa girare il serpente alla propria destra rispetto alla direzione attuale\n
        Se direzione attuale = [x,y], ``turn_right()`` ritorna [-y,x]
        
        **Esempio:**
        Se [0,1] (giu') e' la direzione attuale, [-1,0] (destra) e' la nuova direzione
        """
        temp = self.direction[0]
        self.direction[0] = -self.direction[1]
        self.direction[1] = temp

    def turn_left(self):
        """
        Fa girare il serpente alla propria destra rispetto alla direzione attuale\n
        Se direzione attuale = [x,y], ``turn_left()`` ritorna [y,-x]
        """
        temp = self.direction[0]
        self.direction[0] = self.direction[1]
        self.direction[1] = -temp

    def AI(self):
        """
        Decide la direzione del serpente in base alla sua attuale visione della mappa\n
        Il neurone di output piu' attivato e' la sua decisione
        """
        decision = np.argmax(self.neural_net.feed_forward(self.vision))
        if decision == 1:
            self.turn_right()
        elif decision == 2:
            self.turn_left()

    def fitness(self):
        """
        Misura quanto e' stato bravo il serpente come funzione della propria lunghezza ed eta'

        :return (int): Punteggio (fitness)
        """
        return (len(self.body)**2) * self.age

    def render(self, window):
        """
        Renderizza la mappa (sfondo, pareti e cibo) nella finestra di gioco e chiama ``render()`` del serpente

        :param window: Finestra di gioco
        """
        body = pygame.image.load(IMAGE_SNAKE).convert_alpha()                   # caricamento immagine
        for block in self.body:
            window.blit(body, (block[0]*SPRITE_SIZE, block[1]*SPRITE_SIZE))     # rendering del serpente
        if self.neural_net:                                                     # chiama il rendering della rete neurale a destra della finestra
            self.neural_net.render(window, self.vision)
