"""
main.py
~~~~~~~~~~

File main del progetto

Puoi decidere di eseguire una rete neurale o di startare l'algoritmo genetico per generare weights & biases,
decommentare cio' che serve e commentare cio' che non serve
"""
from game import *
from genetic_algorithm import *

"""
Decommentare le reti che si vogliono eseguire
"""
net = NeuralNetwork()
game = Game()

# # Giuseppe (NON VA MOLTO BENE 5/10)
# net.load(filename_weights='saved/giuseppe_weights.npy', filename_biases='saved/giuseppe_biases.npy')
# game.start(display=True, neural_net=net)

# # Francesco (VA MOLTO BENE 8/10 SICURO E PRECISO)
# net.load(filename_weights='saved/francesco_weights.npy', filename_biases='saved/francesco_biases.npy')
# game.start(display=True, neural_net=net)

# # Luca (VA IN LOOP MOLTO SPESSO MA QUANDO NON CI VA E' IL MIGLIORE 7/10)
# net.load(filename_weights='saved/luca_weights.npy', filename_biases='saved/luca_biases.npy')
# game.start(display=True, neural_net=net)

# # Nicola (VA BENE 8/10)
# net.load(filename_weights='saved/nicola_weights.npy', filename_biases='saved/nicola_biases.npy')
# game.start(display=True, neural_net=net)

# # Ylena (VA BENE 6/10)
# net.load(filename_weights='saved/ylena_weights.npy', filename_biases='saved/ylena_biases.npy')
# game.start(display=True, neural_net=net)

# # Giovanni (VA BENE 7/10)
# net.load(filename_weights='saved/giovanni_weights.npy', filename_biases='saved/giovanni_biases.npy')
# game.start(display=True, neural_net=net)

# # Aldo (VA BENE MA SPESSO EVITA IL CIBO NEGLI ANGOLI 7/10)
# net.load(filename_weights='saved/aldo_weights.npy', filename_biases='saved/aldo_biases.npy')
# game.start(display=True, neural_net=net)

# # Ivan (MEDIOCRE 4/10)
# net.load(filename_weights='saved/ivan_weights.npy', filename_biases='saved/ivan_biases.npy')
# game.start(display=True, neural_net=net)

# # Tony (VA BENINO MA GIRA SOLO A DESTRA 6/10)
# net.load(filename_weights='saved/tony_weights.npy', filename_biases='saved/tony_biases.npy')
# game.start(display=True, neural_net=net)



"""
Decommenta per giocare a snake
"""

# game = Game()
# game.start(playable=True, display=True, speed=10)
  
"""
Algoritmo genetico

Decommentare per trainare delle nuove reti neurali
"""
# gen = GeneticAlgorithm(population_size=1000, crossover_method='layer', mutation_method='neuron', generation_number=100)
# gen.start()


game.endGame() # Chiude pygame