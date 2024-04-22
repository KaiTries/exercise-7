import math
import random
import tsplib95

# Class representing the environment of the ant colony
"""
    rho: pheromone evaporation rate
"""
class Environment:
    def __init__(self,tsp: str, rho: float, ant_population: int):
        self.tsp = tsp
        self.rho = rho
        self.ant_population = ant_population

        # initialize env topology
        self.problem = tsplib95.load(tsp)
        self.nodes = list(self.problem.get_nodes())
        self.edges = self.problem.get_edges()

        self.pheromone_map = {}
        self.distance_map = {}

        # initialize phereomone map
        self.initialize_distance_map()
        self.initialize_pheromone_map()

        self.update_pheromone_map(None)

    
    def initialize_distance_map(self):
        for edge in self.edges:
            self.distance_map[(edge[0],edge[1])] = self._get_distance(edge[0],edge[1])

    # Intialize the pheromone trails in the environment
    def initialize_pheromone_map(self) -> None:
        curr_node = random.randint(1,48)
        cost = 0
        visited = []

        while (len(visited) < 48):
            visited.append(curr_node)
            closest = float("inf")
            next_node = None
            for n in range(1, 48):
                if n not in visited:
                    dist = self.get_distance(curr_node,n)
                    if dist < closest:
                        closest = dist
                        next_node = n
                        cost += dist
            if next_node:
                curr_node = next_node

        visited.append(visited[0])
        cost += self.get_distance(curr_node, visited[0])

        print("initial pheromone per edge: ", self.ant_population / cost)

        for edge in self.edges:
            self.pheromone_map[(edge[0],edge[1])] = self.ant_population / cost
            

    # Update the pheromone trails in the environment
    def update_pheromone_map(self, ants: list) -> None:
        for edge in self.pheromone_map:
            self.pheromone_map[edge] *= (1 - self.rho)

        for ant in ants:
            for c in range(len(ant.visited) - 1):
                i = ant.visited[c]
                j = ant.visited[c + 1]
                self.pheromone_map[(i,j)] += 1 / self.get_distance(i,j)
        
    # Get the pheromone trails in the environment
    def get_pheromone_map(self):
        pass

    # Get the environment topology
    def get_possible_locations(self, current_location: int):
        pass

    # Get the pseudo-euclidean distance between two vertices
    def get_distance(self, i, j):
        return self.distance_map[(i,j)]


    def _get_distance(self, i: int, j: int) -> int:
        return tsplib95.distances.pseudo_euclidean(self.problem.node_coords[i],self.problem.node_coords[j],round=math.ceil)