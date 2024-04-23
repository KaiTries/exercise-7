cmake_minimum_required(VERSION 3.10)  # Set the minimum version of CMake

project(AntColonyOptimization)  # Define the project name

set(CMAKE_CXX_STANDARD 17)  # Set the C++ standard
set(CMAKE_CXX_STANDARD_REQUIRED True)

# List all your .cpp files involved in the build
add_executable(AntColonyOptimization Ant_colony.cpp Ant.cpp Environment.cpp)

include_directories(${PROJECT_SOURCE_DIR}/include)
