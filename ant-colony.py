import numpy as np
import random

from environment import Environment
from ant import Ant 

# Class representing the ant colony
"""
    ant_population: the number of ants in the ant colony
    iterations: the number of iterations 
    alpha: a parameter controlling the influence of the amount of pheromone during ants' path selection process
    beta: a parameter controlling the influence of the distance to the next node during ants' path selection process
    rho: pheromone evaporation rate
"""
class AntColony:
    def __init__(self, ant_population: int, iterations: int, alpha: float, beta: float, rho: float):
        self.ant_population = ant_population
        self.iterations = iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho 

        # Initialize the environment of the ant colony
        self.environment = Environment(self.rho, ant_population)

        # Initilize the list of ants of the ant colony
        self.ants = []

        # Initialize the ants of the ant colony
        for i in range(ant_population):
            
            # Initialize an ant on a random initial location 
            ant = Ant(self.alpha, self.beta, random.randint(1,48))

            # Position the ant in the environment of the ant colony so that it can move around
            ant.join(self.environment)
        
            # Add the ant to the ant colony
            self.ants.append(ant)

    # Solve the ant colony optimization problem  
    def solve(self):
        # The solution will be a list of the visited cities
        solution = []

        # Initially, the shortest distance is set to infinite
        shortest_distance = np.inf

        # we doing x amount of rounds
        for _ in range(0,self.iterations):
            # each ant runs its path
            for ant in self.ants:
                ant.run()
                # if an ant found a new shortest path we set it
                if ant.travelled_distance < shortest_distance:
                    solution = ant.visited
                    shortest_distance = ant.travelled_distance
            # update the pheromone map
            self.environment.update_pheromone_map(self.ants)
            # reset the memory of the ants (distance travelled and citys visited)
            for ant in self.ants:
                ant.reset_ant()



        return solution, shortest_distance


def main():
    # Intialize the ant colony
    ant_colony = AntColony(48, 100, 1, 2, 0.5)

    # Solve the ant colony optimization problem
    solution, distance = ant_colony.solve()
    print("Solution: ", solution)
    print("Distance: ", distance)


if __name__ == '__main__':
    main()    