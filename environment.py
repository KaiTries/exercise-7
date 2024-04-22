import math
import tsplib95
import numpy as np

# Class representing the environment of the ant colony
"""
    rho: pheromone evaporation rate
"""
class Environment:
    def __init__(self, rho, ant_population):

        self.rho =rho
        self.ant_population = ant_population
        # Initialize the environment topology
        self.problem = tsplib95.load("./att48-specs/att48.tsp")
        
        self.distances = np.full((self.problem.dimension, self.problem.dimension), 0)
        self.pheromones = None

        # Intialize the pheromone map in the environment
        self.initialize_distance_map()
        self.initialize_pheromone_map()

    def initialize_distance_map(self):
        for i in range(self.problem.dimension):
            for j in range(self.problem.dimension):
                if i != j:
                    self.distances[i][j] = self.problem.get_weight(i+1,j+1)

    # Intialize the pheromone trails in the environment
    def initialize_pheromone_map(self):
        current_node = 0
        cost = 0
        visited = []

        while len(visited) < 48:
            visited.append(current_node)
            closest = float("inf")
            next_node = None
            for n in range(self.problem.dimension):
                if n not in visited:
                    dist = self.distances[current_node][n]
                    if dist < closest:
                        closest = dist
                        next_node = n
                        cost += dist
            if next_node:
                current_node = next_node
        
        visited.append(visited[0])
        cost += self.distances[current_node][visited[0]]
        
        
        print("initial pheromone per trail: ", self.ant_population / cost)

        self.pheromones = np.full((self.problem.dimension, self.problem.dimension), self.ant_population / cost)

        

    # Update the pheromone trails in the environment
    def update_pheromone_map(self, ants: list):
        # Step 1: Evaporate
        self.pheromones *= (1 - self.rho)

        # Step 2: Deposit
        for ant in ants:
            for i in range(len(ant.path)-1):
                self.pheromones[ant.path[i]][ant.path[i + 1]] += 1 / ant.travelled_distance
                self.pheromones[ant.path[i + 1]][ant.path[i]] += 1 / ant.travelled_distance
        
    # Get the pheromone trails in the environment
    def get_pheromone_map(self):
        return self.pheromones
    
    def get_distance_map(self):
        return self.distances
    

    