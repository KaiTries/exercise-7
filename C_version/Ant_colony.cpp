#include <iostream>
#include <vector>
#include <limits>
#include <random>
#include <cmath> // For std::pow, std::numeric_limits<double>::infinity()

#include "Ant.h"  // Assume Ant class is defined in Ant.h
#include "Environment.h" // Assume Environment class is defined in Environment.h


class AntColony {
private:
    int ant_population;
    int iterations;
    double alpha, beta, rho;
    Environment environment;
    std::vector<Ant> ants;

public:
    AntColony(int _ant_population, int _iterations, double _alpha, double _beta, double _rho)
        : ant_population(_ant_population), iterations(_iterations), alpha(_alpha), beta(_beta), rho(_rho), 
          environment(_rho, _ant_population) {
        // Initialize ants with random start locations
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> dis(1, environment.n);

        // initialize the ants vector to the correct size
        ants.reserve(ant_population);
        
        // print the number of cities

        for (int i = 0; i < ant_population; ++i) {
            Ant newAnt = Ant(alpha, beta, dis(gen));
            newAnt.join(&environment);
            ants.emplace_back(newAnt);
        }
    }

    std::pair<std::vector<int>, double> solve() {
        std::vector<int> best_solution;
        double best_distance = std::numeric_limits<double>::infinity();

        for (int i = 0; i < iterations; ++i) {
            for (auto& ant : ants) {
                ant.run();
                if (ant.travelled_distance < best_distance) {
                    best_distance = ant.travelled_distance;
                    best_solution = ant.visited_locations;
                }
            }
            environment.update_pheromone_map(ants);
        }
        return {best_solution, best_distance};
    }
};


int main() {
    const int ants = 10, iterations = 10, iterations_per_level = 1;
    const std::vector<double> alphas = {0.75, 1, 1.25};
    const std::vector<double> betas = {2, 3, 5, 6};
    const std::vector<double> rhos = {0.1, 0.3, 0.5, 0.8};

    double best_distance = std::numeric_limits<double>::infinity();
    std::vector<int> best_solution;
    double alpha_best, beta_best, rho_best;

    for (auto alpha : alphas) {
        for (auto beta : betas) {
            for (auto rho : rhos) {
                std::cout << "Alpha: " << alpha << " Beta: " << beta << " Rho: " << rho << std::endl;

                for (int i = 0; i < iterations_per_level; ++i) {
                    AntColony colony(ants, iterations, alpha, beta, rho);
                    auto [solution, distance] = colony.solve();

                    if (distance < best_distance) {
                        best_distance = distance;
                        best_solution = solution;
                        alpha_best = alpha;
                        beta_best = beta;
                        rho_best = rho;

                        std::cout << "New best distance: " << best_distance << std::endl;
                    }
                }
            }
        }
    }

    std::cout << "Best settings: Alpha = " << alpha_best << ", Beta = " << beta_best << ", Rho = " << rho_best << std::endl;
    std::cout << "Best solution distance: " << best_distance << std::endl;
    std::cout << "Solution path: ";
    for (auto city : best_solution) {
        std::cout << city << " ";
    }
    std::cout << std::endl;

    return 0;
}
