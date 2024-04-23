#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <limits>
#include <random>
#include <string>
#include <iomanip>

#include "environment.h"
#include "ant.h"


Environment::Environment(double _rho, int _ant_population) 
    : rho(_rho), ant_population(_ant_population) {
    // print the number of cities
    load_problem("att48.tsp");  // Specify the path to your TSPLIB file
    initialize_pheromone_values();
}

void Environment::load_problem(const std::string& filename) {
    // load a file  assuming it is in the same folder:
    std::ifstream file(filename);

    if (!file) {
        std::cerr << "Error: file not found" << std::endl;
        return;
    }

    std::string line;
    while (std::getline(file, line)) {
        if (line == "NODE_COORD_SECTION") {
            break;
        }
    }

    int id;
    double x, y;
    while (file >> id >> x >> y) {
        nodes.push_back({id, x, y});
    }

    n = nodes.size();
    file.close();

    // Create edges
    for (int i = 1; i <= n; ++i) {
        for (int j = i + 1; j <= n; ++j) {
            // i want to set the distance to the actual distance between the two node with id i and j
            int distance = get_distance(i - 1, j - 1);
            edges.push_back({i, j, distance, 0});
        }
    }
}

void Environment::initialize_pheromone_values() {
    // initialize it with a nearest neighbour heuristic
    int current_node = 1;
    int cost = 0;
    std::vector<int> visited;
    visited.push_back(current_node);

    while (visited.size() < n) {
        int min_distance = std::numeric_limits<int>::max();
        int next_node = -1;

        for (auto &node : nodes) {
            if (node.id == current_node || std::find(visited.begin(), visited.end(), node.id) != visited.end()) {
                continue;
            }
            int distance = get_distance(current_node - 1, node.id - 1);
            if (distance < min_distance) {
                min_distance = distance;
                next_node = node.id;
            }
        }
        visited.push_back(next_node);
        cost += min_distance;
        if (next_node != -1) current_node = next_node;
    }

    // Calculate the initial pheromone value
    double initial_pheromone = static_cast<double>(ant_population) / cost;

    for (auto& edge : edges) {
        edge.pheromone = initial_pheromone;
    }
    // print the initial pheromone value make sure it is printed with 10 places after the decimal point
    std::cout << "Initial pheromone value: " << initial_pheromone << std::endl;
}

double Environment::get_distance(int i, int j) {
    // Calculate and return the distance.
    // the parameters are the ids of the two nodes
    auto& node1 = nodes[i];
    auto& node2 = nodes[j];
    double dist = std::sqrt(std::pow(node1.x - node2.x, 2) + std::pow(node1.y - node2.y, 2));
    return std::round(dist);
}

void Environment::update_pheromone_map(const std::vector<Ant>& ants) {
    // Evaporate old pheromone
    for (auto &edge : edges) {
        edge.pheromone *= (1.0 - rho);
        std::cout << "Pheromone value before: " << edge.pheromone << std::endl;
    }

    // Add new pheromone based on the ants' paths
    for (auto &ant : ants) {
        double additional_pheromone = 1.0 / ant.travelled_distance;

        for (size_t i = 0; i < ant.get_visited_locations().size() - 1; ++i) {
            int from = ant.get_visited_locations()[i];
            int to = ant.get_visited_locations()[i + 1];
            edges[from - 1].pheromone += additional_pheromone;
            edges[to - 1].pheromone += additional_pheromone;
        }
    }

    // print the pheromone values
    for (auto &edge : edges) {
        std::cout << "Pheromone value after: " << edge.pheromone << std::endl;
    }
}