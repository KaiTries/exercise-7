# Class representing an artificial ant of the ant colony
"""
    alpha: a parameter controlling the influence of the amount of pheromone during ants' path selection process
    beta: a parameter controlling the influence of the distance to the next node during ants' path selection process
"""
class Ant():
    def __init__(self, alpha: float, beta: float, initial_location: int):
        self.alpha = alpha
        self.beta = beta
        self.current_location = initial_location
        self.visited = [initial_location]
        self.travelled_distance = 0

       # The ant runs to visit all the possible locations of the environment 
    def run(self):
        while len(self.visited) < 48:
            next_node = self.select_path()
            self.travelled_distance += self.get_distance(next_node)
            self.visited.append(next_node)
            self.current_location = next_node
                
    # Select the next path based on the random proportional rule of the ACO algorithm
    def select_path(self):
        reachable_cities = self.environment.get_possible_locations(self.current_location)
        not_yet_visited = {key: value for key, value in reachable_cities.items() if key not in self.visited}
        
        denominator = 0

        for city in not_yet_visited:
            pheromone_level = not_yet_visited[city]["pheromone_level"]
            distance_heuristic = 1 / not_yet_visited[city]["weight"]
            not_yet_visited[city]["numerator"] = pheromone_level**self.alpha * distance_heuristic**self.beta
            denominator += not_yet_visited[city]["numerator"]

        for city in not_yet_visited:
            not_yet_visited[city]["probability"] = not_yet_visited[city]["numerator"] / denominator

        return max(not_yet_visited, key=lambda x: not_yet_visited[x]["probability"])


    def get_cost(self):
        return self.travelled_distance

    # Position an ant in an environment
    def join(self, environment):
        self.environment = environment
        self.select_path()

    # Get the pseudo-euclidean distance between current location and the destination vertex
    def get_distance(self, j: int):
        return self.environment.get_distance(self.current_location, j)
    
    def reset_ant(self):
        self.visited = [self.current_location]
        self.travelled_distance = 0
