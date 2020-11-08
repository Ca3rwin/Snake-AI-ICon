"""
main.py
~~~~~~~~~~

File main del progetto

Puoi decidere di eseguire una rete neurale o di startare l'algoritmo genetico per generare weights & biases,
decommentare ciò che serve e commentare ciò che non serve
"""
from game import*
from genetic_algorithm import *


"""
Watch games of snake played by my best neural nets !

Only 3 games are played here but you can load more networks from the saved folder if you wish
"""
net = NeuralNetwork()
game = Game()

# # Joseph (NON VA MOLTO BENE 5/10) is the funniest to watch, he always does something cool
# net.load(filename_weights='saved/joseph_weights.npy', filename_biases='saved/joseph_biases.npy')
# game.start(display=True, neural_net=net)

# # Valentin (VA MOLTO BENE 8/10) is safe and precise
# net.load(filename_weights='saved/valentin_weights.npy', filename_biases='saved/valentin_biases.npy')
# game.start(display=True, neural_net=net)

# # Larry (VA IN LOOP PORCODIO 3/10) is very very safe but also my best network, don't hesitate to run him a few times if he's doing loops
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

# net.load(filename_weights='a_gen_10_weights.npy', filename_biases='a_gen_1_biases.npy')
# game.start(display=True, neural_net=net)


"""
Play a game of snake !

I do not recommend it as it is in first person and not that fun
But if you want, you can
"""

# game = Game()
# game.start(playable=True, display=True, speed=10)
  
"""
Train your own snakes !

Starts the genetic algorithm with parameters that I've already tested
Best snake of each generation is saved in current folder
The training speed depend a lot on your CPU and its cores number

Contact me if you know how to make it run on GPU
"""
gen = GeneticAlgorithm(population_size=1000, crossover_method='neuron', mutation_method='weight')
gen.start()

# Hey pssst, you, yes you.. Sometimes I boost training by making the snake already huge at the begining
# Also don't hesitate to put a iteration limit in the game loop (see game.py)

game.endGame()