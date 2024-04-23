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
        self.environment = Environment(self.rho, self.ant_population)

        # Initilize the list of ants of the ant colony
        self.ants = []

        # Initialize the ants of the ant colony
        for i in range(ant_population):
            # Initialize an ant on a random initial location 
            ant = Ant(self.alpha, self.beta, random.choice(range(self.environment.n)))
            ant.join(self.environment)
            self.ants.append(ant)

    # Solve the ant colony optimization problem  
    def solve(self):
        # The solution will be a list of the visited cities
        solution = []
        # Initially, the shortest distance is set to infinite
        shortest_distance = np.inf
        # Iterate over the number of iterations
        for i in range(self.iterations):
            # Run all the ants of the ant colony
            for ant in self.ants:
                ant.run()
                # Check if the ant found a better solution
                if ant.travelled_distance < shortest_distance:
                    shortest_distance = ant.travelled_distance
                    solution = ant.visited_locations
            # Update the pheromone map of the environment
            self.environment.update_pheromone_map(self.ants)
        return solution, shortest_distance


def main():
    random.seed(1337)
    # ant colony configuration
    ants = 48
    iterations_per_level = 50
    iterations = 100

    alphas = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5]
    betas = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6]
    rhos = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    results = {
        "Best": {
            "Alpha": None,
            "Beta": None,
            "Rho": None,
            "Solution": None,
            "Distance": None
        }    
    }

    best_distance = np.inf
    for alpha in alphas:
        for beta in betas:
            for rho in rhos:
                print("Alpha: ", alpha)
                print("Beta: ", beta)
                print("Rho: ", rho)
                for i in range(iterations_per_level):
                    ant_colony = AntColony(ants, iterations, alpha, beta, rho)
                    # Solve the ant colony optimization problem
                    solution, distance = ant_colony.solve()
                    if distance < best_distance:
                        best_distance = distance
                        results["Best"]["Alpha"] = alpha
                        results["Best"]["Beta"] = beta
                        results["Best"]["Rho"] = rho
                        results["Best"]["Solution"] = solution
                        results["Best"]["Distance"] = distance
                        print("Best solution: ", solution)
                        print("Best distance: ", distance)
            

    print(results)

if __name__ == '__main__':
    main()    