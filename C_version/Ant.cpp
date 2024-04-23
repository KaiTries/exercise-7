#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <set>
#include <map>
#include "ant.h"
#include "environment.h"

using namespace std;
std::mt19937 Ant::gen(std::random_device{}());


Ant::Ant(double _alpha, double _beta, int initial_location) 
    : alpha(_alpha), beta(_beta), current_location(initial_location), travelled_distance(0.0) {}

vector<vector<double>> Ant::precompute_probability_matrix() {
    const auto& edges = environment->edges; // reference to the edges in the environment

    vector<vector<double>> probabilities(environment->n, vector<double>(environment->n, 0.0)); // initialize a 2D vector of size n x n

    // p_ij = (pheromones_ij ** alpha) * (1 / distance_ij ** beta)

    for (auto&edge :edges) {
        double pheromone = edge.pheromone;
        double distance = 1.0 / get_distance(edge.from - 1, edge.to - 1);
        // Here we have to do both directions because the graph is undirected
        probabilities[edge.from - 1][edge.to - 1] = pow(pheromone, alpha) * pow(distance, beta); // p_ij = (pheromones_ij ** alpha) * (1 / distance_ij ** beta)
        probabilities[edge.to - 1][edge.from - 1] = pow(pheromone, alpha) * pow(distance, beta); // p_ji = (pheromones_ji ** alpha) * (1 / distance_ji ** beta)
    } 

    return probabilities; // return the 2D vector of probabilities
}

void Ant::run() {
    // clear visited locations and edges
    this->visited_locations.clear();
    this->visited_edges.clear();
    this->travelled_distance = 0.0;

    // add initial location to visited locations
    visited_locations.push_back(current_location);

    vector<int> not_yet_visited;

    for (int i = 1; i < environment->n + 1; ++i) {
        // if i is not in visited_locations, add it to not_yet_visited
        if (find(visited_locations.begin(), visited_locations.end(), i) != visited_locations.end()) continue;
        not_yet_visited.push_back(i);
    }

    auto probabilities = precompute_probability_matrix(); 

    while (visited_locations.size() < 48) { 
        int next_location = select_path(not_yet_visited, probabilities);
        travelled_distance += get_distance(current_location - 1, next_location - 1); // nodes are 1-indexed, so we subtract 1
        visited_locations.push_back(next_location);
        visited_edges.emplace_back(current_location, next_location);

        current_location = next_location;
        not_yet_visited.erase(remove(not_yet_visited.begin(), not_yet_visited.end(), next_location), not_yet_visited.end());

    }
    // Return to the initial location
    travelled_distance += get_distance(visited_locations.back() - 1, visited_locations.front() - 1);
    visited_edges.emplace_back(visited_locations.back(), visited_locations.front());
    visited_locations.push_back(visited_locations.front());
}

double Ant::get_distance(int i, int j) {
    return environment->get_distance(i, j); // return the distance between node i and node j
}



int Ant::select_path(const vector<int>& not_yet_visited, const vector<vector<double>>& probabilities) {
    std::vector<double> _probabilities(not_yet_visited.size()); // initialize a vector of size not_yet_visited.size()

    double sum_probabilities = 0.0;

    for (size_t index = 0; index < not_yet_visited.size(); ++index) {
        int j = not_yet_visited[index]; // get the index of the next location
        double probability = probabilities[current_location - 1][j - 1]; // get the probability of moving from the current location to the next location
        _probabilities[index] = probability; // set the probability in the vector
        sum_probabilities += _probabilities[index]; // add the probability to the sum
    }

    for (double &prob : _probabilities) {
        prob /= sum_probabilities; // divide each probability by the sum of probabilities
    }

    std::uniform_real_distribution<double>dist(0.0,1.0); // initialize a uniform real distribution between 0 and 1
    double choice = dist(gen); // generate a random number between 0 and 1
    double cumulative = 0.0;

    for (size_t index = 0; index < _probabilities.size(); ++index) { // iterate over the probabilities
        cumulative += _probabilities[index]; // add the probability to the cumulative
        if (choice <= cumulative) { // if the choice is less than or equal to the cumulative
            return not_yet_visited[index]; // return the next location
        }
    }
    return not_yet_visited.back();
}






void Ant::join(Environment* env) {
    environment = env;
}
