#ifndef ENVIRONMENT_H
#define ENVIRONMENT_H

#include <vector>
#include <random>

class Ant;

struct Edge {
    int from;
    int to;
    int distance;
    double pheromone;
};

struct Node {
    int id;
    double x;
    double y;
};

class Environment {
public:
    double rho;
    int ant_population;
    int n;
    std::vector<Node>nodes;
    std::vector<Edge>edges;

    Environment(double _rho, int _ant_population);
    void initialize_pheromone_values();
    void update_pheromone_map(const std::vector<Ant>& ants);
    double get_distance(int i, int j);
    void load_problem(const std::string& filename);
};

#endif // ENVIRONMENT_H
