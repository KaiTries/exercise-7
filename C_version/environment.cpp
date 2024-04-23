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


std::mt19937 Environment::gen(std::random_device{}());



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
            int distance = get_distance(i - 1, j - 1);
            edges.push_back({i, j, distance, 0});
        }
    }
}

/*
    * Initialize the pheromone values for each edge
    * The pheromone value is initialized to the inverse of the cost of a random path
    * The cost of the path is calculated by selecting the nearest neighbour for each node
    * The pheromone value is then calculated by dividing the number of ants by the cost of the path
    * The pheromone value is then set for each edge
*/
void Environment::initialize_pheromone_values() {
    std::uniform_int_distribution<> distrib(1, 48); 
    int current_node = distrib(gen);  // Generates a random start node between 1 and 48

    int cost = 0; // The cost of the path
    std::vector<int> visited; // The nodes that have been visited
    visited.push_back(current_node); // Add the start node to the visited nodes

    while (visited.size() < n) {
        int min_distance = std::numeric_limits<int>::max();
        int next_node = -1;

        for (auto &node : nodes) {
            if (node.id == current_node || std::find(visited.begin(), visited.end(), node.id) != visited.end()) // Skip the current node and already visited nodes
            { 
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
        if (next_node != -1) current_node = next_node; // Update the current node
    }

    cost += get_distance(visited.back() - 1, visited.front() - 1); // Add the distance from the last node to the first node

    // Calculate the initial pheromone value
    double initial_pheromone = static_cast<double>(ant_population) / cost; 

    for (auto& edge : edges) {
        edge.pheromone = initial_pheromone; // Set the initial pheromone value for each edge
    }    
}

double Environment::get_distance(int i, int j) {
    // calculate the pseudo euclidean distance
    auto& node1 = nodes[i];
    auto& node2 = nodes[j];

    if (node1.id != i + 1 || node2.id != j + 1) {
        std::cerr << "Error: node id does not match index" << std::endl;
    }

    double xd = node1.x - node2.x;
    double yd = node1.y - node2.y;

    double rij = std::sqrt((xd * xd + yd * yd) / 10.0);
    double tij = std::round(rij);

    if (tij < rij) {
        return tij + 1;
    }
    return tij;
}

void Environment::update_pheromone_map(const std::vector<Ant>& ants) {
    // Evaporate old pheromone
    for (auto &edge : edges) {
        edge.pheromone *= (1.0 - rho);
    }

    // Add new pheromone based on the ants' paths
    for (auto &ant : ants) {
        double additional_pheromone = 1.0 / ant.travelled_distance; // The amount of pheromone to add
        const auto& visited_locations = ant.get_visited_locations(); // The nodes visited by the ant

        for (size_t k = 0; k < visited_locations.size() - 1; ++k) {
            int i = visited_locations[k];
            int j = visited_locations[k + 1];
            if (i >= j) {
                std::swap(i, j); // Ensure that i < j
            }

            // transform 2D index to 1D index
            int index = ((i - 1) * n) - ((i - 1) * ((i - 1) + 1) / 2);
            index += ((j - 1) - (i - 1) - 1);

            if (edges[index].from != i || edges[index].to != j) {
                std::cerr << "Error: edge does not match given from and to" << std::endl;
            }

            edges[index].pheromone += additional_pheromone; // Add the pheromone to the edge
        }
    }
}