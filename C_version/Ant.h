#ifndef ANT_H
#define ANT_H

#include "Environment.h"
#include <vector>
#include <set>

class Ant {
public:
    double alpha, beta;
    int current_location;
    double travelled_distance;
    std::vector<int> visited_locations;
    std::vector<std::vector<double>> probabilities;
    std::vector<std::pair<int, int>> visited_edges;
    Environment* environment;
    static std::mt19937 gen;

    Ant(double _alpha, double _beta, int initial_location);
    void join(Environment* env);
    std::vector<std::vector<double>> precompute_probability_matrix();
    void run();
    int select_path(const std::vector<int>& not_yet_visited, const std::vector<std::vector<double>>& probabilities);
    double get_distance(int i, int j);
    std::vector<int> get_visited_locations() const { return visited_locations; }
};

#endif // ANT_H
