import math
import tsplib95


# Class representing an artificial ant of the ant colony
"""
    alpha: a parameter controlling the influence of the amount of pheromone during ants' path selection process
    beta: a parameter controlling the influence of the distance to the next node during ants' path selection process
"""
class Ant():
    def __init__(self, alpha: float, beta: float, initial_location):
        self.alpha = alpha
        self.beta = beta
        self.current_location = initial_location
        self.travelled_distance = 0
        self.environment = None

    # The ant runs to visit all the possible locations of the environment 
    def run(self):
        pass

    def get_distance(self,i,j):
        # Get the distance between two nodes
        return tsplib95.distances.pseudo_euclidean(self.environment.node_coords[i], self.environment.node_coords[j], math.ceil)

    # Select the next path based on the random proportional rule of the ACO algorithm
    def select_path(self):
        pass

    # Position an ant in an environment
    def join(self, environment):
        self.environment = environment
