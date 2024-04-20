import math
import random
import tsplib95

# Class representing the environment of the ant colony
"""
    rho: pheromone evaporation rate
"""
class Environment:
    def __init__(self, rho: float, ant_population: int):
        self.rho =rho
        self.population = ant_population
        # Initialize the environment topology
        self.environment = tsplib95.load('att48-specs/att48.tsp').get_graph()
        # Intialize the pheromone map in the environment
        self.initialize_pheromone_map()
    

    # Intialize the pheromone trails in the environment
    def initialize_pheromone_map(self) -> None:
        # C^nn is the expected cost of a tour generated using a nearest neighbour heuristic
        current_node = random.randint(1,48)
        starting_node = current_node
        cost = 0
        visited = []
        # loop until all nodes have been visited. Add up the cost
        # cost is just the distance
        while len(visited) < 48:
            visited.append(current_node)
            closest = float("inf")
            next_node = None
            for n in self.environment.neighbors(current_node):
                if n not in visited:
                    dist = self.get_distance(current_node,n)
                    if dist < closest:
                        closest = dist
                        next_node = n
                        cost += dist
            if next_node:
                current_node = next_node
        
        visited.append(starting_node)
        cost += self.get_distance(current_node,starting_node)
        
        
        print("initial pheromone per trail: ", self.population / cost)
            
        for edge in self.environment.edges():
            self.environment[edge[0]][edge[1]]["pheromone_level"] = 1 / cost
            

    # Update the pheromone trails in the environment
    def update_pheromone_map(self, ants: list) -> None:
        # Step 1: Pheromone is first removed from all arcs (pheromone evaporation):
        for edge in self.environment.edges():
            self.environment[edge[0]][edge[1]]["pheromone_level"] *= (1- self.rho)

        # Step 2: Pheromone is then added on the arcs the ants have crossed in their tours:
        for ant in ants:
            for i in range(len(ant.visited)-1):
                self.environment[ant.visited[i]][ant.visited[i + 1]]["pheromone_level"] += 1 / ant.travelled_distance

    # Get the pheromone trails in the environment
    def get_pheromone_map(self):
        return self.environment.edges()
    
    # Get the environment topology
    def get_possible_locations(self, current_location: int):
        return self.environment[current_location]
    
    # Get the pseudo-euclidean distance between two vertices
    def get_distance(self, i: int, j: int) -> int:
        return self.environment[i][j]["weight"]
