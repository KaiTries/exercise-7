#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <set>
#include <map>
#include "Ant.h"
#include "Environment.h"

using namespace std;

Ant::Ant(double _alpha, double _beta, int initial_location) 
    : alpha(_alpha), beta(_beta), current_location(initial_location), travelled_distance(0.0) {}

vector<vector<double>> Ant::precompute_probability_matrix() {
    const auto& edges = environment->edges;

    vector<vector<double>> probabilities(environment->n, vector<double>(environment->n, 0.0));

    // the probability of going from i to j is given by the formula
    // p_ij = (pheromone_jj ^alpa) * (1/d_ij ^ beta) / sum(pheromone_jj ^ alpha * 1/d_ij ^ beta)
    double sum = 0.0;
    for (auto&edge :edges) {
        double pheromone = edge.pheromone;
        double distance = 1.0 / get_distance(edge.from - 1, edge.to - 1);
        sum += pow(pheromone, alpha) * pow(distance, beta);
    }

    for (int i = 0; i < environment->n; ++i) {
        for (int j = 0; j < environment->n; ++j) {
            double pheromone = edges[i].pheromone;
            double distance = 1.0 / get_distance(i, j);
            probabilities[i][j] = (pow(pheromone, alpha) * pow(distance, beta)) / sum;
        }
    }

    return probabilities;
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
        travelled_distance += get_distance(current_location - 1, next_location - 1);
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
    return environment->get_distance(i, j);
}



int Ant::select_path(const vector<int>& not_yet_visited, const vector<vector<double>>& probabilities) {
    // from the probabilites matrix choose the vector corresponding to the current location
    // and select the next location based on the probabilities
    vector<int> choices = not_yet_visited;
    vector<double> probabilities_for_current_location = probabilities[current_location - 1];
    vector<double> probabilities_for_choices;

    for (int i = 0; i < choices.size(); ++i) {
        probabilities_for_choices.push_back(probabilities_for_current_location[choices[i] - 1]);
    }
    
    // normalize the probabilities
    double sum = 0.0;
    for (auto& prob : probabilities_for_choices) {
        sum += prob;
    }

    vector<double> normalized_probabilities;
    for (auto& prob : probabilities_for_choices) {
        normalized_probabilities.push_back(prob / sum);
    }

    // select the next location based on the probabilities
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<double> dis(0.0, 1.0);
    double random_number = dis(gen);

    double cumulative_probability = 0.0;
    for (int i = 0; i < normalized_probabilities.size(); ++i) {
        cumulative_probability += normalized_probabilities[i];
        if (random_number <= cumulative_probability) {
            return choices[i];
        }
    }
    return choices.back();
}

void Ant::join(Environment* env) {
    environment = env;
}
