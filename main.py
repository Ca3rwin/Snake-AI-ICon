"""
main.py
~~~~~~~~~~

File main del progetto

Puoi decidere di eseguire una rete neurale o di startare l'algoritmo genetico per generare weights & biases,
decommentare cio' che serve e commentare cio' che non serve
"""
from game import *
from genetic_algorithm import *

def load_ivan():
    """ Carica ed esegue pesi e bias del migliore di ognuna delle 10 generazioni di Ivan """
    
    net.load(filename_weights='saved/ivan(200,layer,neuron,10)/gen_1_weights.npy',
          filename_biases='saved/ivan(200,layer,neuron,10)/gen_1_biases.npy')
    game.start(display=True, neural_net=net)
    net.load(filename_weights='saved/ivan(200,layer,neuron,10)/gen_2_weights.npy',
          filename_biases='saved/ivan(200,layer,neuron,10)/gen_2_biases.npy')
    game.start(display=True, neural_net=net)
    net.load(filename_weights='saved/ivan(200,layer,neuron,10)/gen_3_weights.npy',
              filename_biases='saved/ivan(200,layer,neuron,10)/gen_3_biases.npy')
    game.start(display=True, neural_net=net)
    net.load(filename_weights='saved/ivan(200,layer,neuron,10)/gen_4_weights.npy',
              filename_biases='saved/ivan(200,layer,neuron,10)/gen_4_biases.npy')
    game.start(display=True, neural_net=net)
    net.load(filename_weights='saved/ivan(200,layer,neuron,10)/gen_5_weights.npy',
              filename_biases='saved/ivan(200,layer,neuron,10)/gen_5_biases.npy')
    game.start(display=True, neural_net=net)
    net.load(filename_weights='saved/ivan(200,layer,neuron,10)/gen_6_weights.npy',
              filename_biases='saved/ivan(200,layer,neuron,10)/gen_6_biases.npy')
    game.start(display=True, neural_net=net)
    net.load(filename_weights='saved/ivan(200,layer,neuron,10)/gen_7_weights.npy',
              filename_biases='saved/ivan(200,layer,neuron,10)/gen_7_biases.npy')
    game.start(display=True, neural_net=net)
    net.load(filename_weights='saved/ivan(200,layer,neuron,10)/gen_8_weights.npy',
              filename_biases='saved/ivan(200,layer,neuron,10)/gen_8_biases.npy')
    game.start(display=True, neural_net=net)
    net.load(filename_weights='saved/ivan(200,layer,neuron,10)/gen_9_weights.npy',
              filename_biases='saved/ivan(200,layer,neuron,10)/gen_9_biases.npy')
    game.start(display=True, neural_net=net)
    net.load(filename_weights='saved/ivan(200,layer,neuron,10)/gen_10_weights.npy',
              filename_biases='saved/ivan(200,layer,neuron,10)/gen_10_biases.npy')
    game.start(display=True, neural_net=net)

"""
Decommentare le reti che si vogliono eseguire
"""
net = NeuralNetwork()
game = Game()

# # Joseph (NON VA MOLTO BENE 5/10)
# net.load(filename_weights='saved/joseph_weights.npy', filename_biases='saved/joseph_biases.npy')
# game.start(display=True, neural_net=net)

# # Valentin (VA MOLTO BENE 8/10 SICURO E PRECISO)
# net.load(filename_weights='saved/valentin_weights.npy', filename_biases='saved/valentin_biases.npy')
# game.start(display=True, neural_net=net)

# # Larry (VA IN LOOP MOLTO SPESSO MA QUANDO NON CI VA E' IL MIGLIORE 5/10)
# net.load(filename_weights='saved/larry_weights.npy', filename_biases='saved/larry_biases.npy')
# game.start(display=True, neural_net=net)

# # Adam (VA BENE 7/10)
# net.load(filename_weights='saved/adam_weights.npy', filename_biases='saved/adam_biases.npy')
# game.start(display=True, neural_net=net)

# # Jason (VA BENE 6/10)
# net.load(filename_weights='saved/jason_weights.npy', filename_biases='saved/jason_biases.npy')
# game.start(display=True, neural_net=net)

# # Juan (VA BENE 7/10)
# net.load(filename_weights='saved/juan_weights.npy', filename_biases='saved/juan_biases.npy')
# game.start(display=True, neural_net=net)

# # Kevin (VA BENE MA SPESSO EVITA IL CIBO NEGLI ANGOLI 7/10)
# net.load(filename_weights='saved/kevin_weights.npy', filename_biases='saved/kevin_biases.npy')
# game.start(display=True, neural_net=net)

# # Ivan (CARICA 10 GENERAZIONI - SOLO L'ULTIMA GEN VA BENE 6/10)
# load_ivan()


"""
Decommenta per giocare a snake
"""

# game = Game()
# game.start(playable=True, display=True, speed=10)
  
"""
Algoritmo genetico

Decommentare per trainare delle nuove reti neurali
"""
# gen = GeneticAlgorithm(population_size=1000, crossover_method='neuron', mutation_method='weight', generation_number=10)
# gen.start()


game.endGame() # Chiude pygame