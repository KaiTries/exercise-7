import numpy as np

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
    def __init__(self, tsp: str, ant_population: int, iterations: int, alpha: float, beta: float, rho: float):
        self.tsp = tsp
        self.ant_population = ant_population
        self.iterations = iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho 

        # Initialize the environment of the ant colony
        self.environment = Environment(self.tsp, self.rho, self.ant_population)

        # Initilize the list of ants of the ant colony
        self.ants = []

        # Initialize the ants of the ant colony
        for i in range(ant_population):
            
            # Initialize an ant on a random initial location 
            ant = Ant(self.alpha, self.beta, None)

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

        return solution, shortest_distance


def main():
    # Intialize the ant colony
    ant_colony = AntColony("./att48-specs/att48.tsp",1, 1, 1, 2, 0.5)

    # Solve the ant colony optimization problem
    solution, distance = ant_colony.solve()
    print("Solution: ", solution)
    print("Distance: ", distance)


if __name__ == '__main__':
    main()    