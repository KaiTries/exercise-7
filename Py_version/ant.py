import tsplib95
import numpy as np

# Class representing an artificial ant of the ant colony
"""
    alpha: a parameter controlling the influence of the amount of pheromone during ants' path selection process
    beta: a parameter controlling the influence of the distance to the next node during ants' path selection process
"""
class Ant():
    def __init__(self, alpha: float, beta: float, initial_location: int):
        self.alpha = alpha
        self.beta = beta
        self.current_location = initial_location + 1
        self.travelled_distance = 0
        self.visited_locations = []
        self.visited_edges = []
        self.environment = None


    def precompute_probability_matrix(self):
        initial_pheromones = self.environment.pheromone_map
        intial_distances = self.environment.distances
    
        # Avoid division by zero: replace zeros in distances with a small value
        safe_distances = np.where(intial_distances == 0, np.inf, intial_distances)

        # this calculates the probabilities based on the ACO algorithm
        # the probability of moving from node i to node j is given by:
        # (pheromone[i, j] ** alpha) * ((1 / distance[i, j]) ** beta)
        probabilities = (initial_pheromones ** self.alpha) * ((1 / safe_distances) ** self.beta)


        return probabilities
        
   
    # The ant runs to visit all the possible locations of the environment 
    def run(self):
        # list of all nodes
        all_cities = [i+1 for i in range(self.environment.n)]
        # precalculate the pheromone matrix
        self.probabilities = self.precompute_probability_matrix()

        # Initialize the ant by visiting the initial location
        self.visited_locations = [self.current_location]
        self.travelled_distance = 0

        # not yet visited nodes
        not_yet_visited = set(all_cities) - set(self.visited_locations)

        while not_yet_visited:
            next_location = self.select_path(list(not_yet_visited))
            self.travelled_distance += self.get_distance(self.current_location, next_location)
            self.visited_locations.append(next_location)
            self.visited_edges.append((self.current_location, next_location))

            # Move to the next location
            self.current_location = next_location
            not_yet_visited.remove(next_location)

        # Return to the initial location
        self.travelled_distance += self.get_distance(self.visited_locations[-1], self.visited_locations[0])
        self.visited_edges.append((self.visited_locations[-1], self.visited_locations[0]))
        self.visited_locations.append(self.visited_locations[0])
        
                
    # Select the next path based on the random proportional rule of the ACO algorithm
    def select_path(self, not_yet_visited):
        # gives us the probability of moving to each node as a vector
        prob_vector = self.probabilities[self.current_location, not_yet_visited]
        total = np.sum(prob_vector)
        normalized_probabilities = prob_vector / total if total > 0 else prob_vector
        return np.random.choice(not_yet_visited, p=normalized_probabilities)
    

    # Position an ant in an environment
    def join(self, environment):
        self.environment = environment


    def get_distance(self, i, j):
        return self.environment.distances[i, j]

