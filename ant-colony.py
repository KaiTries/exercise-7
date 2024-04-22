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
    ants = 10
    iterations_per_level = 50
    iterations = 20

    results = {
        "Alpha": {
            "range" : {},
            "best": ()
        },
        "Beta": {
            "range": {},
            "best": ()
        },
        "Rho": {
            "range": {},
            "best": ()
        }
    }
    
    # Test the influence of the alpha parameter
    for alpha in np.arange(0, 5.5, 0.5):
        print("Alpha: ", alpha)
        distances = []
        best_distance = np.inf
        best_solution = None
        for i in range(iterations_per_level):
            ant_colony = AntColony(ants, iterations, alpha, 2, 0.5)
            # Solve the ant colony optimization problem
            solution, distance = ant_colony.solve()
            distances.append(distance)
            if distance < best_distance:
                best_distance = distance
                best_solution = solution
        results["Alpha"]["range"][alpha] = sum(distances) / len(distances)
        results["Alpha"]["best"] = (best_solution, best_distance)
    
    # choose the best alpha and beta from the results
    alpha = min(results["Alpha"]["range"], key=results["Alpha"]["range"].get)
    print("Best alpha: ", alpha)

    # Test the influence of the beta parameter
    for beta in np.arange(2, 5.5, 0.5):
        print("Beta: ", beta)
        distances = []
        best_distance = np.inf
        best_solution = None
        for i in range(iterations_per_level):
            ant_colony = AntColony(ants, iterations, alpha, beta, 0.5)
            # Solve the ant colony optimization problem
            solution, distance = ant_colony.solve()
            distances.append(distance)
            if distance < best_distance:
                best_distance = distance
                best_solution = solution
        results["Beta"]["range"][beta] = sum(distances) / len(distances)
        results["Beta"]["best"] = (best_solution, best_distance)

    # choose the best alpha and beta from the results
    beta = min(results["Beta"]["range"], key=results["Beta"]["range"].get)
    print("Best beta: ", beta)


    for rho in np.arange(0, 1, 0.1):
        print("Rho: ", rho)
        distances = []
        best_distance = np.inf
        best_solution = None
        for i in range(iterations_per_level):
            ant_colony = AntColony(ants, iterations, alpha, beta, rho)
            # Solve the ant colony optimization problem
            solution, distance = ant_colony.solve()
            distances.append(distance)
            if distance < best_distance:
                best_distance = distance
                best_solution = solution
        results["Rho"]["range"][rho] = sum(distances) / len(distances)
        results["Rho"]["best"] = (best_solution, best_distance)

    # choose the best rho from the results
    rho = min(results["Rho"]["range"], key=results["Rho"]["range"].get)
    print("Best rho: ", rho)



    print(results)

if __name__ == '__main__':
    main()    