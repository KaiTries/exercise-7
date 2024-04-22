import tsplib95
import numpy as np
# Class representing an artificial ant of the ant colony
"""
    alpha: a parameter controlling the influence of the amount of pheromone during ants' path selection process
    beta: a parameter controlling the influence of the distance to the next node during ants' path selection process
"""
class Ant():
    def __init__(self, alpha: float, beta: float, initial_location):
        self.alpha = alpha
        self.beta = beta
        self.current_location = initial_location + 1
        self.travelled_distance = 0
        self.visited_locations = []
        self.visited_edges = []
        self.environment = None


    # The ant runs to visit all the possible locations of the environment 
    def run(self):
        # list of all nodes
        all_cities = [i+1 for i in range(self.environment.n)]
        # Initialize the ant by visiting the initial location
        self.visited_locations = [self.current_location]
        self.travelled_distance = 0

        # not yet visited nodes
        not_yet_visited = set(all_cities) - set(self.visited_locations)

        while not_yet_visited:
            next_location = self.select_path(not_yet_visited)
            self.travelled_distance += self.get_distance(self.current_location, next_location)
            self.visited_locations.append(next_location)
            self.visited_edges.append((self.current_location, next_location))

            # Move to the next location
            self.current_location = next_location
            not_yet_visited.remove(next_location)

        # Return to the initial location
        self.travelled_distance += self.get_distance(self.visited_locations[-1], self.visited_locations[0])
        self.visited_edges.append((self.visited_locations[-1], self.visited_locations[0]))



    # Select the next path based on the random proportional rule of the ACO algorithm
    def select_path(self, not_yet_visited):
        # Calculate the probability of selecting each path
        probabilities = self.get_probabilities(not_yet_visited)

        # Select the next path based on the probability
        next_location = np.random.choice(list(not_yet_visited), p=probabilities)
        return next_location
    

    # Calculate the probabilities of selecting paths
    def get_probabilities(self, not_yet_visited):
        probabilities = []
        total = 0
        for i in not_yet_visited:
            total += self.get_probability(i)
            probabilities.append(self.get_probability(i))

        for k in range(len(probabilities)):
            probabilities[k] /= total
        
        return probabilities
    
    # Calculate the probability of selecting a path
    def get_probability(self, i):
        return (self.environment.pheromone_map[(self.current_location, i)] ** self.alpha) * ((1 / self.get_distance(self.current_location, i)) ** self.beta)



    # Position an ant in an environment
    def join(self, environment):
        self.environment = environment
    
    def get_distance(self, i, j):
        return tsplib95.distances.pseudo_euclidean(self.environment.problem.node_coords[i], self.environment.problem.node_coords[j])
