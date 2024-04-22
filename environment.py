import math
import random
import tsplib95

# Class representing the environment of the ant colony
"""
    rho: pheromone evaporation rate
"""
class Environment:
    def __init__(self, rho, ant_population: int):

        self.rho =rho
        self.ant_population = ant_population
        
        # Initialize the environment topology
        self.problem = tsplib95.load("./att48-specs/att48.tsp")
        self.n = self.problem.dimension
        self.nodes = list(self.problem.get_nodes())
        self.edges = list(self.problem.get_edges())


        # Initialize the pheromone map in the environment
        self.distances =  self.initialize_distance_matrix()
        self.pheromone_map = self.initialize_pheromone_map()

    
    # Initialize the distance matrix of the environment
    def initialize_distance_matrix(self):
        distances = {}
        for i in range(self.n):
            for j in range(self.n):
                distances[(i + 1, j + 1)] = self.get_distance(i + 1, j + 1)
        return distances




    # Intialize the pheromone trails in the environment
    def initialize_pheromone_map(self):
        # find cost of tour that uses nearest neighbor heuristic
        curr_node = random.choice(self.nodes)
        cost = 0
        visited = [curr_node]

        while len(visited) < self.n:
            min_dist = math.inf
            min_node = -1
            for node in self.nodes:
                if node not in visited:
                    dist = self.distances[(curr_node, node)]
                    if dist < min_dist:
                        min_dist = dist
                        min_node = node
            visited.append(min_node)
            cost += min_dist
            curr_node = min_node

        cost += self.distances[(visited[-1], visited[0])]

        # initial pheromone is given by m / C^nn where m is the number of ants and C^nn is the cost of the nearest neighbor tour
        initial_pheromone = self.ant_population / cost

        print("Initial pheromone: ", initial_pheromone)

        pheromone_map = {}
        for edge in self.edges:
            pheromone_map[edge] = initial_pheromone
        return pheromone_map
    
        

    # Update the pheromone trails in the environment
    def update_pheromone_map(self, ants: list):
        # Step 1: Evaporate pheromone
        for edge in self.edges:
            self.pheromone_map[edge] *= (1 - self.rho)
        
        # Step 2: Deposit pheromone
        for ant in ants:
            for edge in ant.visited_edges:
                self.pheromone_map[edge] += 1 / ant.travelled_distance
                # also add the reverse edge
                self.pheromone_map[(edge[1], edge[0])] += 1 / ant.travelled_distance
        
      


    # Get the pheromone trails in the environment
    def get_pheromone_map(self):
        return self.environment.edges()
    
    # Get the environment topology
    def get_possible_locations(self):
        pass

    # specific pseudo euclidean distance
    def get_distance(self, i, j):
        return tsplib95.distances.pseudo_euclidean(self.problem.node_coords[i], self.problem.node_coords[j])
    
    # Get the pseudo-euclidean distance between two vertices
    def get_distance(self, i: int, j: int) -> int:
        return self.environment[i][j]["weight"]
