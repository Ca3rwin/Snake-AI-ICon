"""
genetic_algorithm.py
~~~~~~~~~~

Modulo che implementa un algoritmo genetico per allenare le reti neurali a giocare a snake
I genitori sono selezionati fra i migliori, si fa un crossover + mutazione
"""

import copy
import multiprocessing
from random import randint
from game import*
from neural_network import *
from joblib import Parallel, delayed


class GeneticAlgorithm:
    """ Genetic Algorithm Class """

    def __init__(self, networks=None, networks_shape=None, population_size=1000, generation_number = 100,
                 crossover_rate=0.3, crossover_method='neuron', mutation_rate=0.7, mutation_method='weight'):
        """
        Inizializzazione della classe GeneticAlgorithm
        
        :param networks (lista di NeuralNetwork): Neural net di prima generazione
        :param networks_shape (lista di int): Definisce il numero di layer e il numero di neuroni per ogni layer (default e' [21, 16, 3])
        :param population_size (int): Numero di neural net per ogni generazione (default e' 1000)
        :param generation_number (int): Per quante generazioni andra' avanti l'algoritmo (default e' 100)
        :param crossover_rate (int): Proporzione su quanti figli creare ad ogni generazione (default e' 0.3)
        :param crossover_method (str): Come verranno generati i figli (default e' 'neuron')
        :param mutation_rate (int): Proporzione su quanta popolazione verra' mutata ad ogni generazione (default e' 0.7)
        :param mutation_method (str): Come verra' fatta la mutazione (default e' 'weight')
        """
        self.networks_shape = networks_shape
        if self.networks_shape is None:             # se non e' passata nessuna morfologia della neural net
            self.networks_shape = [21,16,3]         # morfologia di default
        
        self.networks = networks
        if networks is None:                                  # se non e' passasta nessuna neural net
            self.networks = []
            for i in range(population_size):                  # genera la popolazione
                self.networks.append(NeuralNetwork(self.networks_shape))

        self.population_size = population_size
        self.generation_number = generation_number
        self.crossover_rate = crossover_rate
        self.crossover_method = crossover_method
        self.mutation_rate = mutation_rate
        self.mutation_method = mutation_method

    def start(self):
        """
        Funzione main per l'algoritmo genetico, alcuni step sono in thread

        Steps ad ogni generazione:\n
        - Selezione parenti
        - Generazione figli
        - Generazione individui mutati
        - Valutazione dell'intera popolazione (vecchia popolazione + figli + individui mutati)
        - Altre mutazioni su individui casuali (migliora il learning)
        - Mantenimento degli individui di *population_size*, scarto dei peggiori

        :return: Niente
        """
        networks = self.networks
        population_size = self.population_size
        crossover_number = int(self.crossover_rate*self.population_size)   # calcola il numero di figli da generare
        mutation_number = int(self.mutation_rate*self.population_size)     # calcola il numero di individui da mutare

        num_cores = multiprocessing.cpu_count()         # numero di core della CPU per mandare in parallelo alcuni step
        gen = 0                                         # generazione attuale
        for i in range(self.generation_number):
            gen += 1

            parents = self.parent_selection(networks, crossover_number, population_size)       # selezione genitori
            children = self.children_production(crossover_number, parents)                     # generazione figli
            mutations = self.mutation_production(networks, mutation_number, population_size)   # mutazioni

            networks = networks + children + mutations                      # vecchia popolazione + individui nuovi
            self.evaluation(networks, num_cores)                            # valutazione delle neural net
            networks.sort(key=lambda Network: Network.score, reverse=True)  # classificazione delle neural net
            networks[0].save(name="gen_"+str(gen))                          # salvataggio delle reti migliori della generazione

            for i in range(int(0.2*len(networks))):              # altre piccole mutazioni casuali per maggior efficienza
                rand = randint(10, len(networks)-1)
                networks[rand] = self.mutation(networks[rand])

            networks = networks[:population_size]       # mantiene solo i migliori individui
            self.print_generation(networks, gen)

    def parent_selection(self, networks, crossover_number, population_size):
        """
        Funzione di selezione dei parenti, 3 individui casuali e li mette in competizione classificandoli
        in base al loro fitness, il migliore viene selezionato come genitore

        :param networks: lista di neural net
        :param crossover_number: numero di genitori necessari
        :param population_size: dimensioni della popolazione
        :return: lista di genitori selezionati
        """
        parents = []
        for i in range(crossover_number):
            parent = self.tournament(networks[randint(0, population_size - 1)],      # esecuzione del "torneo"
                                     networks[randint(0, population_size - 1)],
                                     networks[randint(0, population_size - 1)])
            parents.append(parent)                                                   # mette in append il genitore vincitore
        return parents

    def children_production(self, crossover_number, parents):
        """
        Prende casualmente 2 genitori nella lista di genitori e ci fa un crossover,
        generando un figlio

        :param crossover_number: numero di figli necessari
        :param parents: lista di genitori
        :return: lista di figli generati
        """
        children = []
        for i in range(crossover_number):
            child = self.crossover(parents[randint(0, crossover_number - 1)],       # generazione figlio
                                   parents[randint(0, crossover_number - 1)])
            children.append(child)                                                  # mette in append il figlio
        return children

    def mutation_production(self, networks, mutation_number, population_size):
        """
        Produce nuovi individui dalla popolazione attuale mutandoli\n
        NB: non modifica gli individui attuali ma ne crea di nuovi

        :param networks: lista di neural net
        :param mutation_number: numero di individui da mutare
        :param population_size: dimensioni della popolazione
        :return: lista di nuovi individui (mutati)
        """
        mutations = []
        for i in range(mutation_number):
            mut = self.mutation(networks[randint(0, population_size - 1)])      # generazione individuo mutato
            mutations.append(mut)                                               # mette in append l'individuo mutato
        return mutations

    def evaluation(self, networks, num_cores, ):
        """
        Prende la popolazione di neural net e gli fa giocare 4 partite a testa,
        il punteggio di una neural net e' la media delle 4 partite\n
        NB: le 4 partite sono parallelizzate usando joblib

        :param networks: lista di neural net
        :param num_cores: numero di core della CPU
        :return: niente ma ogni neural_net in 'networks' e' stata valutata (in neural_net.score)
        """
        game = Game()
        results1 = Parallel(n_jobs=num_cores)(delayed(game.start)(neural_net=networks[i]) for i in range(len(networks)))
        results2 = Parallel(n_jobs=num_cores)(delayed(game.start)(neural_net=networks[i]) for i in range(len(networks)))
        results3 = Parallel(n_jobs=num_cores)(delayed(game.start)(neural_net=networks[i]) for i in range(len(networks)))
        results4 = Parallel(n_jobs=num_cores)(delayed(game.start)(neural_net=networks[i]) for i in range(len(networks)))
        for i in range(len(results1)):
            networks[i].score = int(np.mean([results1[i], results2[i], results3[i], results4[i]]))

    def tournament(self, net1, net2, net3):
        """
        Prende 3 neural net, gli fa giocare una partita a testa e seleziona chi performa meglio

        :param net1: neural net (primo partecipante)
        :param net2: neural net (secondo partecipante)
        :param net3: neural net (terzo partecipante)
        :return: la neural net vincitrice
        """
        game = Game()
        game.start(neural_net=net1)                 # net1 gioca la partita
        score1 = game.game_score
        game.start(neural_net=net2)                 # net2 gioca la partita
        score2 = game.game_score
        game.start(neural_net=net3)                 # net3 gioca la partita
        score3 = game.game_score
        maxscore = max(score1, score2, score3)      # il miglior score viene ritornato
        if maxscore == score1:
            return net1
        elif maxscore == score2:
            return net2
        else:
            return net3

    def crossover(self, net1, net2):
        """
        Prende due neural net e produce un figlio in base al metodo contenuto in self.crossover_method

        Esempio di come funziona (method = 'neuron'):\n
        - Due network vengono creati (copie dei rispettivi genitori)
        - Seleziona un neurone casuale in un layer casuale OPPURE un bias casuale in un layer casuale
        - Scambia il neurone o bias fra le due neural net
        - Ogni neural net gioca una partita
        - La migliore viene selezionata
        Il principio e' lo stesso per i metodi 'weight' o 'layer'        

        :param net1: neural net (genitore 1)
        :param net2: neural net (genitore 2)
        :return: neural net (figlio)
        """
        res1 = copy.deepcopy(net1)                 # copia i parenti (che saranno i due figli), altrimenti manipoleremmo i veri parenti
        res2 = copy.deepcopy(net2)
        weights_or_biases = random.randint(0, 1)   # sceglie casualmente se il crossover e' fra pesi/neuroni/layer OPPURE fra bias
        if weights_or_biases == 0:                 # crossover fra pesi/neuroni/layer
            if self.crossover_method == 'weight':
                layer = random.randint(0, len(res1.weights) - 1)                            # layer casuale
                neuron = random.randint(0, len(res1.weights[layer]) - 1)                    # neurone casuale
                weight = random.randint(0, len(res1.weights[layer][neuron]) - 1)            # peso casuale
                temp = res1.weights[layer][neuron][weight]                                  # scambio dei pesi
                res1.weights[layer][neuron][weight] = res2.weights[layer][neuron][weight]
                res2.weights[layer][neuron][weight] = temp
            elif self.crossover_method == 'neuron':
                layer = random.randint(0, len(res1.weights) - 1)                            # layer casuale
                neuron = random.randint(0, len(res1.weights[layer]) - 1)                    # neurone casuale
                temp = copy.deepcopy(res1)                                                  # scambio dei neuroni
                res1.weights[layer][neuron] = res2.weights[layer][neuron]
                res2.weights[layer][neuron] = temp.weights[layer][neuron]
            elif self.crossover_method == 'layer':
                layer = random.randint(0, len(res1.weights) - 1)                            # layer casuale
                temp = copy.deepcopy(res1)                                                  # scambio dei layer
                res1.weights[layer] = res2.weights[layer]
                res2.weights[layer] = temp.weights[layer]
        else:                                                       # crossover fra bias
            layer = random.randint(0, len(res1.biases) - 1)         # layer casuale
            bias = random.randint(0, len(res1.biases[layer]) - 1)   # bias casuale
            temp = copy.deepcopy(res1)                              # scambio dei bias
            res1.biases[layer][bias] = res2.biases[layer][bias]
            res2.biases[layer][bias] = temp.biases[layer][bias]

        game = Game()
        game.start(neural_net=res1)     # figlio 1 gioca una partita
        score1 = game.game_score
        game.start(neural_net=res2)     # figlio 2 gioca una partita
        score2 = game.game_score
        if score1 > score2:             # ritorna il migliore
            return res1
        else:
            return res2

    def mutation(self, net):
        """
        Prende una rete neurale e ne crea una copia con una mutazione in base al metodo contenuto in
        self.mutation_method

        :param net: neural net che sara' copiata
        :return: neural net uguale al param net, fatta eccezione per le parti mutate
        """
        res = copy.deepcopy(net)                    # crea una copia altrimenti manipoliamo la rete reale
        weights_or_biases = random.randint(0, 1)    # sceglie casualmente se la mutazione e' su peso/neurone OPPURE su bias
        if weights_or_biases == 0:                  # mutazione su peso/neurone
            if self.mutation_method == 'weight':
                layer = random.randint(0, len(res.weights) - 1)                  # layer casuale
                neuron = random.randint(0, len(res.weights[layer]) - 1)          # neurone casuale
                weight = random.randint(0, len(res.weights[layer][neuron]) - 1)  # peso casuale
                res.weights[layer][neuron][weight] = np.random.randn()           # mutazione
            elif self.mutation_method == 'neuron':
                layer = random.randint(0, len(res.weights) - 1)                  # layer casuale
                neuron = random.randint(0, len(res.weights[layer]) - 1)          # neurone casuale
                new_neuron = np.random.randn(len(res.weights[layer][neuron]))    
                res.weights[layer][neuron] = new_neuron                          # mutazione
        else:                                                      # mutazione su bias
            layer = random.randint(0, len(res.biases) - 1)         # layer casuale
            bias = random.randint(0, len(res.biases[layer]) - 1)   # bias casuale
            res.weights[layer][bias] = np.random.randn()           # mutazione
        return res

    def print_generation(self, networks, gen):
        """   
        Stampa informazioni sulla generazione attuale:\n
        - Miglior fitness
        - Dimensioni della popolazione
        - Media dei top 6
        - Media dei bottom 6
        """
        top_mean = int(np.mean([networks[i].score for i in range(6)]))
        bottom_mean = int(np.mean([networks[-i].score for i in range(1, 6)]))
        print("\nBest Fitness gen", gen, " : ", networks[0].score)
        print("Pop size = ", len(networks))
        print("Average top 6 = ", top_mean)
        print("Average last 6 = ", bottom_mean)
