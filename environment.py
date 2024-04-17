import math
import tsplib95

# Class representing the environment of the ant colony
"""
    rho: pheromone evaporation rate
"""
class Environment:
    def __init__(self, rho):

        self.rho =rho
        
        # Initialize the environment topology
        self.environment = tsplib95.load('att48-specs/att48.tsp')
        self.environment.get_edges()
        # Intialize the pheromone map in the environment
        self.pheromone_map = {}
        self.initialize_pheromone_map()
    

    # Intialize the pheromone trails in the environment
    def initialize_pheromone_map(self):
        pass


    # Update the pheromone trails in the environment
    def update_pheromone_map(self):
        pass

    # Get the pheromone trails in the environment
    def get_pheromone_map(self):
        pass
    
    # Get the environment topology
    def get_possible_locations(self):
        pass
    
