import random
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
        self.path = []
        self.travelled_distance = 0

    # The ant runs to visit all the possible locations of the environment 
    def run(self):
        # start at first node
        self.path = [self.current_location]
        self.travelled_distance = 0

        # create a set of nodes not yet visited
        not_yet_visited = set(range(48)) - set(self.path)
        
        # while there are still nodes left to explore
        while not_yet_visited:
            # select next node
            next_node = self.select_path(not_yet_visited)
            # add distance to that node to the total cost
            self.travelled_distance += self.get_distance(next_node)
            # remove the node from the set
            not_yet_visited.remove(next_node)
            # add it to the tour
            self.path.append(next_node)
        
        # add the distance from last node back to first node
        self.travelled_distance += self.get_distance(self.path[0])
        # add first node again
        self.path.append(self.path[0])


    # Select the next path based on the random proportional rule of the ACO algorithm
    def select_path(self, not_yet_visited):

        pheromone_map = self.environment.pheromones
        distances_map = self.environment.distances

        probabilites = []
        divisor = 0

        for city in not_yet_visited:
            pheromone_level = pheromone_map[self.current_location][city]
            distance_heuristic = distances_map[self.current_location][city]

            probability = pheromone_level**self.alpha * distance_heuristic**self.beta
            divisor += pheromone_level**self.alpha * distance_heuristic**self.beta
            probabilites.append(probability)

        for i in range(len(probabilites)):
            probabilites[i] /= divisor
        
        return random.choices(list(not_yet_visited),weights=probabilites,k=1)[0]

    # Position an ant in an environment
    def join(self, environment):
        self.environment = environment

    def get_distance(self,to):
        return self.environment.distances[self.current_location][to]