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
    # ant colony configuration
    ants = 48
    iterations_per_level = 20
    iterations = 50


    results = {
        "Alpha": {
            "range" : {}
        },
        "Beta": {
            "range": {}
        },
        "Rho": {
            "range": {}
        },
        "Best": {
            "Alpha": None,
            "Beta": None,
            "Rho": None,
            "Solution": None
        }
    }
    for alpha in [0.75,1,1.25]:
        for beta in [2,3,4,5,6]:
            for rho in [0.3,0.4,0.5,0.6,0.7]:
                print("Alpha: ", alpha)
                print("Beta: ", beta)
                print("Rho: ", rho)
                distances = []
                best_distance = np.inf
                for i in range(iterations_per_level):
                    ant_colony = AntColony(ants, iterations, alpha, beta, rho)
                    # Solve the ant colony optimization problem
                    solution, distance = ant_colony.solve()
                    distances.append(distance)
                    if distance < best_distance:
                        best_distance = distance
                        results["Best"]["Alpha"] = alpha
                        results["Best"]["Beta"] = beta
                        results["Best"]["Rho"] = rho
                        results["Best"]["Solution"] = solution
                

                print("Average distance: ", sum(distances) / len(distances))
                print("Best distance: ", best_distance)


    print(results)

if __name__ == '__main__':
    main()    