#include <iostream>
#include <iomanip>
#include <vector>
#include <limits>
#include <random>
#include <cmath>

#include "ant.h"
#include "environment.h"

void display_progress_and_results(
    bool flag,
    std::vector<int> best_solution,
    int current_iteration, 
    int total_iterations, 
    double best_distance, 
    double best_alpha, 
    double best_beta, 
    double best_rho,
    double alpha,
    double beta,
    double rho
) {
    if (flag) {
        // Move cursor up three lines
        std::cout << "\x1b[3A";
    } else {
        std::cout << std::string(100, ' ') << "\r";  // Assume 100 is more than enough to clear any previous content
    }
    // Overwrite the best distance and parameter line
    std::cout << "\r" << std::flush;
    std::cout << "Best Distance: " << best_distance << " (α=" << best_alpha << ", β=" << best_beta << ", ρ=" << best_rho << ")" << std::endl;

    // overwrite the the array with the best path
    std::cout << "Best Path: ";
    for (auto city : best_solution) {
        std::cout << city << " ";
    }
    std::cout << std::endl;




    // Overwrite the progress and current parameter line
    std::cout << "\r" << std::flush;

    double percentage = 100.0 * current_iteration / total_iterations;

    int bar_width = 50;
    int pos = bar_width * (current_iteration / static_cast<double>(total_iterations));
    std::string arrow = ">";
    if (current_iteration == total_iterations) {
        std::cout << "[" << std::string(pos, '=') << "] " << std::fixed << std::setprecision(2) << percentage << "%";
    } else {
        std::cout << "[" << std::string(pos, '=') << arrow << std::string(bar_width - pos - 1, ' ') << "] " << std::fixed << std::setprecision(2) << percentage << "% ";
    }
    std::cout << " Current Parameters: (α=" << alpha << ", β=" << beta << ", ρ=" << rho << ")" << std::endl;

    // Flush to make sure everything is printed out
    std::cout << std::flush;

}

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
    std::mt19937 generator(1);
    const int ants = 48, iterations = 50, iterations_per_level = 10;
    const std::vector<double> alphas = {0.8,0.9,1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2};
    const std::vector<double> betas = {1.5,1.6,1.7,1.8,1.9,2,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3};
    const std::vector<double> rhos = {0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9};

    double best_distance = std::numeric_limits<double>::infinity();
    std::vector<int> best_solution;

    for (int i = 1; i <= 48; ++i) {
        best_solution.push_back(i);
    }
    double alpha_best, beta_best, rho_best;

    display_progress_and_results(false,best_solution,0,iterations_per_level,best_distance,0,0,0,alphas[0],betas[0],rhos[0]);
    for (auto alpha : alphas) {
        for (auto beta : betas) {
            for (auto rho : rhos) {
                for (int i = 1; i <= iterations_per_level; ++i) {
                    AntColony colony(ants, iterations, alpha, beta, rho);
                    auto [solution, distance] = colony.solve();

                    if (distance < best_distance) {
                        best_distance = distance;
                        best_solution = solution;
                        alpha_best = alpha;
                        beta_best = beta;
                        rho_best = rho;
                    }
                    display_progress_and_results(true,best_solution,i,iterations_per_level,best_distance,alpha_best,beta_best,rho_best,alpha,beta,rho);
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
